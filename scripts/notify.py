#!/usr/bin/env python3
"""
Fan a message out to the crew over e-mail (Gmail SMTP) and WhatsApp (CallMeBot).

Everything sensitive comes from the environment, never from a file in the
repo -- this repo is public, so recipient addresses and phone numbers are
treated as secrets too, not just the API keys.

Environment:
    NOTIFY_RECIPIENTS   JSON array, see below (required)
    GMAIL_USER          Gmail address messages are sent from
    GMAIL_APP_PASSWORD  Gmail App Password (not the account password)
    NOTIFY_FROM_NAME    Display name on the e-mail (default: LeetCode Streak Bot)

NOTIFY_RECIPIENTS looks like:

    [
      {"name": "Ömer", "email": "omer@example.com",
       "whatsapp": "+905551112233", "callmebot_apikey": "123456"},
      {"name": "Ali", "email": "ali@example.com"}
    ]

Each field is optional except "name": a recipient with only an e-mail gets
mail, one with only a phone + key gets WhatsApp. CallMeBot issues a separate
apikey per phone number, so both fields must travel together.

Usage:
    python scripts/notify.py --subject "..." --body-file msg.txt
    echo "..." | python scripts/notify.py --subject "..." --body -
    python scripts/notify.py --subject "..." --body "hi" --dry-run

Exits non-zero if any channel failed, after attempting every recipient.
"""
import argparse
import json
import os
import smtplib
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"

# CallMeBot asks for a gap between messages; without it later sends get dropped.
CALLMEBOT_DELAY_SECONDS = 3.0
HTTP_TIMEOUT = 20.0


def mask_email(address: str) -> str:
    """a.person@example.com -> a***n@example.com. Logs are public in Actions."""
    local, _, domain = address.partition("@")
    if not domain:
        return "***"
    if len(local) <= 2:
        return f"{local[:1]}***@{domain}"
    return f"{local[0]}***{local[-1]}@{domain}"


def mask_phone(phone: str) -> str:
    digits = "".join(c for c in phone if c.isdigit())
    return f"***{digits[-4:]}" if len(digits) >= 4 else "***"


def load_recipients(raw: str) -> list:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"NOTIFY_RECIPIENTS is not valid JSON: {exc}")
    if not isinstance(data, list):
        raise SystemExit("NOTIFY_RECIPIENTS must be a JSON array of recipient objects.")

    recipients = []
    for index, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise SystemExit(f"NOTIFY_RECIPIENTS[{index}] must be an object, got {type(entry).__name__}.")
        name = str(entry.get("name") or f"recipient-{index + 1}")
        phone = str(entry.get("whatsapp") or "").strip()
        apikey = str(entry.get("callmebot_apikey") or "").strip()
        if bool(phone) != bool(apikey):
            raise SystemExit(
                f"NOTIFY_RECIPIENTS[{index}] ({name}): 'whatsapp' and 'callmebot_apikey' "
                "must both be set or both be omitted."
            )
        recipients.append({
            "name": name,
            "email": str(entry.get("email") or "").strip(),
            "whatsapp": phone,
            "callmebot_apikey": apikey,
        })
    if not recipients:
        raise SystemExit("NOTIFY_RECIPIENTS is empty -- nobody to notify.")
    return recipients


def send_emails(recipients, subject, body, dry_run=False):
    """Send one message per recipient. Separate sends keep the list private."""
    targets = [r for r in recipients if r["email"]]
    if not targets:
        print("email: no recipients with an address, skipping.")
        return []

    user = os.environ.get("GMAIL_USER", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    from_name = os.environ.get("NOTIFY_FROM_NAME", "LeetCode Streak Bot")

    if not dry_run and not (user and password):
        return [f"email: GMAIL_USER/GMAIL_APP_PASSWORD not set, {len(targets)} recipient(s) skipped."]

    if dry_run:
        for r in targets:
            print(f"email: [dry-run] would send to {r['name']} <{mask_email(r['email'])}>")
        return []

    failures = []
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=HTTP_TIMEOUT) as server:
            server.login(user, password)
            for r in targets:
                message = EmailMessage()
                message["Subject"] = subject
                message["From"] = f"{from_name} <{user}>"
                message["To"] = r["email"]
                message.set_content(f"Selam {r['name']},\n\n{body}\n")
                try:
                    server.send_message(message)
                    print(f"email: sent to {r['name']} <{mask_email(r['email'])}>")
                except smtplib.SMTPException as exc:
                    failures.append(f"email -> {r['name']} <{mask_email(r['email'])}>: {exc}")
    except (smtplib.SMTPException, OSError, ssl.SSLError) as exc:
        # Login/connection died, so nobody got mail -- report the whole batch.
        failures.append(f"email: SMTP connection failed ({exc}); {len(targets)} recipient(s) not notified.")
    return failures


def send_whatsapps(recipients, body, dry_run=False):
    targets = [r for r in recipients if r["whatsapp"]]
    if not targets:
        print("whatsapp: no recipients configured, skipping.")
        return []

    failures = []
    for index, r in enumerate(targets):
        masked = mask_phone(r["whatsapp"])
        if dry_run:
            print(f"whatsapp: [dry-run] would send to {r['name']} ({masked})")
            continue

        query = urllib.parse.urlencode({
            "phone": r["whatsapp"],
            "text": body,
            "apikey": r["callmebot_apikey"],
        })
        request = urllib.request.Request(
            f"{CALLMEBOT_URL}?{query}",
            headers={"User-Agent": "leetcode-streak-bot"},
        )
        try:
            with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
                # CallMeBot answers 200 with an HTML page even for some errors,
                # so the status alone isn't proof of delivery.
                text = response.read().decode("utf-8", errors="replace")
            if "APIKey" in text and "invalid" in text.lower():
                failures.append(f"whatsapp -> {r['name']} ({masked}): CallMeBot rejected the API key.")
            else:
                print(f"whatsapp: sent to {r['name']} ({masked})")
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            failures.append(f"whatsapp -> {r['name']} ({masked}): {exc}")

        if index < len(targets) - 1:
            time.sleep(CALLMEBOT_DELAY_SECONDS)
    return failures


def read_body(value: str) -> str:
    if value == "-":
        return sys.stdin.read()
    return value


def main():
    parser = argparse.ArgumentParser(description="Send a notification over e-mail and WhatsApp.")
    parser.add_argument("--subject", required=True, help="E-mail subject line")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="Message text, or '-' to read stdin")
    group.add_argument("--body-file", help="Read the message text from this file")
    parser.add_argument("--channels", default="email,whatsapp",
                        help="Comma-separated subset of: email, whatsapp (default: both)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Log what would be sent without contacting anyone")
    args = parser.parse_args()

    if args.body_file:
        try:
            body = open(args.body_file, encoding="utf-8").read()
        except OSError as exc:
            sys.exit(f"Could not read --body-file: {exc}")
    else:
        body = read_body(args.body)

    body = body.strip()
    if not body:
        sys.exit("Message body is empty.")

    channels = {c.strip().lower() for c in args.channels.split(",") if c.strip()}
    unknown = channels - {"email", "whatsapp"}
    if unknown:
        sys.exit(f"Unknown channel(s): {', '.join(sorted(unknown))}")

    recipients = load_recipients(os.environ.get("NOTIFY_RECIPIENTS", ""))
    print(f"Notifying {len(recipients)} recipient(s) over: {', '.join(sorted(channels))}")

    failures = []
    if "email" in channels:
        failures += send_emails(recipients, args.subject, body, args.dry_run)
    if "whatsapp" in channels:
        failures += send_whatsapps(recipients, body, args.dry_run)

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        sys.exit(1)
    print("All notifications delivered.")


if __name__ == "__main__":
    main()
