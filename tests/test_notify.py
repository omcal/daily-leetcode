"""Tests for the notifier -- mainly that it never leaks PII into public logs."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import notify  # noqa: E402


def test_mask_email_hides_the_middle():
    masked = notify.mask_email("omerisildak@example.com")
    assert masked == "o***k@example.com"
    assert "omerisildak" not in masked


def test_mask_email_handles_short_locals():
    assert notify.mask_email("ab@example.com") == "a***@example.com"
    assert notify.mask_email("garbage") == "***"


def test_mask_phone_keeps_only_the_last_four():
    masked = notify.mask_phone("+90 555 111 2233")
    assert masked == "***2233"
    assert "555" not in masked


def test_load_recipients_parses_a_full_entry():
    raw = json.dumps([{
        "name": "Ömer", "email": "o@example.com",
        "whatsapp": "+905551112233", "callmebot_apikey": "123456",
    }])
    (recipient,) = notify.load_recipients(raw)
    assert recipient["name"] == "Ömer"
    assert recipient["callmebot_apikey"] == "123456"


def test_load_recipients_allows_email_only():
    (recipient,) = notify.load_recipients(json.dumps([{"name": "Ali", "email": "a@example.com"}]))
    assert recipient["whatsapp"] == ""


def test_phone_without_apikey_is_rejected():
    """CallMeBot keys are per-number, so a lone phone would silently never send."""
    raw = json.dumps([{"name": "Ali", "whatsapp": "+905551112233"}])
    with pytest.raises(SystemExit, match="both be set"):
        notify.load_recipients(raw)


def test_apikey_without_phone_is_rejected():
    raw = json.dumps([{"name": "Ali", "callmebot_apikey": "123456"}])
    with pytest.raises(SystemExit, match="both be set"):
        notify.load_recipients(raw)


@pytest.mark.parametrize("raw, match", [
    ("", "not valid JSON"),
    ("{}", "must be a JSON array"),
    ("[]", "nobody to notify"),
    ('["ali"]', "must be an object"),
])
def test_bad_recipient_payloads_fail_loudly(raw, match):
    with pytest.raises(SystemExit, match=match):
        notify.load_recipients(raw)


def test_dry_run_email_sends_nothing(capsys, monkeypatch):
    monkeypatch.setattr(notify.smtplib, "SMTP_SSL", _explode)
    recipients = notify.load_recipients(json.dumps([{"name": "Ali", "email": "ali@example.com"}]))

    assert notify.send_emails(recipients, "subject", "body", dry_run=True) == []
    assert "a***i@example.com" in capsys.readouterr().out


def test_dry_run_whatsapp_sends_nothing(capsys, monkeypatch):
    monkeypatch.setattr(notify.urllib.request, "urlopen", _explode)
    recipients = notify.load_recipients(json.dumps([{
        "name": "Ali", "whatsapp": "+905551112233", "callmebot_apikey": "k",
    }]))

    assert notify.send_whatsapps(recipients, "body", dry_run=True) == []
    assert "***2233" in capsys.readouterr().out


def test_missing_gmail_credentials_is_reported_not_swallowed(monkeypatch):
    monkeypatch.delenv("GMAIL_USER", raising=False)
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)
    recipients = notify.load_recipients(json.dumps([{"name": "Ali", "email": "ali@example.com"}]))

    failures = notify.send_emails(recipients, "subject", "body")
    assert len(failures) == 1
    assert "GMAIL_USER" in failures[0]


def test_channels_with_no_targets_are_skipped_quietly():
    recipients = notify.load_recipients(json.dumps([{"name": "Ali", "email": "ali@example.com"}]))
    assert notify.send_whatsapps(recipients, "body") == []


def _explode(*args, **kwargs):
    raise AssertionError("dry-run must not touch the network")
