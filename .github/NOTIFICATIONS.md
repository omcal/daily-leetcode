# Streak hatırlatıcısı — kurulum

Her gece **00:05 (TRT)** `Streak Reminder` workflow'u çalışır. `problems/*/notes.md`
frontmatter'ındaki en yeni `date` değerine bakar; bir gün hiç çözüm girilmemişse
listedeki herkese e-posta + WhatsApp mesajı gider.

> **Bu repo public.** Telefon numaraları ve e-posta adresleri de en az API
> anahtarları kadar gizli veri — hiçbiri repo'da bir dosyada tutulmuyor, hepsi
> GitHub Secrets'tan geliyor. Aşağıdaki hiçbir değeri commit'lemeyin.

## 1. Gmail App Password

E-postalar Gmail SMTP üzerinden gider. Normal hesap şifresi çalışmaz, App
Password gerekir:

1. Gönderici olacak Google hesabında **2 adımlı doğrulamayı** açın.
2. https://myaccount.google.com/apppasswords adresinden yeni bir App Password
   üretin (isim: `leetcode-bot` gibi).
3. Çıkan 16 karakterlik değeri not alın — bir daha gösterilmez.

## 2. CallMeBot WhatsApp anahtarı (listedeki **her kişi** ayrı ayrı yapar)

CallMeBot anahtarı telefon numarası başına üretilir, yani mesaj alacak herkesin
kendi telefonundan bir kez izin vermesi gerekir. Güncel adımlar ve bot numarası:
https://www.callmebot.com/blog/free-api-whatsapp-messages/

Özetle: sayfadaki CallMeBot numarasını rehbere ekleyip WhatsApp'tan
`I allow callmebot to send me messages` yazarsınız, bot size `apikey` döner.
Bu anahtarı kişiye özel olarak saklayın.

## 3. GitHub Secrets

Repo → **Settings → Secrets and variables → Actions → New repository secret**.
Üç secret ekleyin:

| Secret | Değer |
|---|---|
| `GMAIL_USER` | Gönderici Gmail adresi, ör. `leetcodebot@gmail.com` |
| `GMAIL_APP_PASSWORD` | 1. adımdaki 16 karakterlik App Password |
| `NOTIFY_RECIPIENTS` | Aşağıdaki JSON |

`NOTIFY_RECIPIENTS` tek satır ya da çok satır JSON olabilir:

```json
[
  {
    "name": "Ömer",
    "email": "omer@example.com",
    "whatsapp": "+905551112233",
    "callmebot_apikey": "123456"
  },
  {
    "name": "Ali",
    "email": "ali@example.com"
  }
]
```

- `name` dışındaki alanlar opsiyonel: sadece `email` varsa yalnız mail gider,
  sadece telefon varsa yalnız WhatsApp.
- `whatsapp` ve `callmebot_apikey` **birlikte** verilmeli. Biri eksikse
  workflow sessizce atlamak yerine hata verir — anahtar tek başına işe yaramaz.
- Telefon numarası ülke koduyla, `+90...` biçiminde.

## 4. README otomatik güncellemesi için izin

`Update README` workflow'u README'yi yeniden üretip repo'ya commit'ler. Bunun
için: **Settings → Actions → General → Workflow permissions → Read and write
permissions**.

## 5. Test edin

Repo → **Actions → Streak Reminder → Run workflow**:

- `dry_run: true` (varsayılan) → kimseye mesaj gitmez, sadece log'a kimin
  bilgilendirileceği yazılır. Adresler `o***r@example.com`, numaralar `***2233`
  şeklinde maskelenir; Actions log'ları public.
- `force: true` → seri kırılmamış olsa bile mesajı üretir. Gerçek gönderim için
  `dry_run`'ı `false` yapın.

Yerelden de test edebilirsiniz. Secret'a yapıştırmadan önce JSON'ı doğrulamak
ve kimin bilgilendirileceğini görmek için:

```bash
NOTIFY_RECIPIENTS='[{"name":"Ben","email":"ben@example.com"}]' python scripts/notify.py --subject test --body test --dry-run
```

Mesaj üretiminden gönderime kadar tam zincir (`--today` ile seri kırılmış gibi
davranır, gerçek tarihe dokunmaz):

```bash
python scripts/check_streak.py --today 2026-12-31 --message-only | NOTIFY_RECIPIENTS='[{"name":"Ben","email":"ben@example.com"}]' python scripts/notify.py --subject "test" --body - --dry-run
```

## Ayarlanabilir şeyler

- **Eşik:** `Run workflow` ekranındaki `max_idle_days` (varsayılan 1). Kalıcı
  değişiklik için `.github/workflows/streak-reminder.yml` içindeki
  `inputs.max_idle_days || '1'` fallback'ini düzenleyin.
- **Saat:** aynı dosyadaki `cron: "5 21 * * *"`. Cron **UTC**'dir; TRT sabit
  UTC+3 olduğu için istediğiniz yerel saatten 3 çıkarın.
- **Mesaj metni:** `scripts/check_streak.py` içindeki `render_message`.

## Bilinmesi gerekenler

- GitHub, cron'ları yoğunluk durumuna göre birkaç dakika geciktirebilir; garanti
  edilen dakika hassasiyeti yoktur.
- Public repo'da 60 gün hiç aktivite olmazsa GitHub zamanlanmış workflow'ları
  otomatik devre dışı bırakır ve uyarı maili atar.
- Fork'lar cron'u devralır ama `if: github.repository == 'omcal/daily-leetcode'`
  koşulu onları durdurur — fork'lardan kimseye mesaj gitmez.
