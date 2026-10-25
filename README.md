# 🔔 Canvas LMS Telegram Bot

Eskişehir Teknik Üniversitesi (ESTÜ) Canvas LMS platformundaki ders duyurularını otomatik olarak takip eden ve **Telegram** üzerinden anlık bildirim gönderen Python tabanlı otomasyon projesi.

## 🚀 Özellikler
* **Bulut Tabanlı Çalışma:** GitHub Actions kullanılarak bilgisayarınız kapalıyken bile 7/24 arka planda çalışır.
* **Akıllı Hafıza Sistemi:** Daha önce gönderilen duyuruları `gonderilen_duyurular.txt` dosyasında saklar, böylece aynı duyuru için tekrar tekrar bildirim atarak spam yapmaz.
* **HTML Temizleme:** Duyuru içeriklerindeki karmaşık HTML etiketlerini temizleyerek okunabilir düz metin halinde iletir.
* **Otomatik Periyot:** Belirli aralıklarla (GitHub Actions cron yardımıyla) derslerinizi güncel olarak tarar.

## 🛠️ Kullanılan Teknolojiler
* **Python** (`canvasapi`, `requests`)
* **GitHub Actions** (CI/CD Otomasyonu ve Zamanlayıcı)
* **Telegram Bot API**

## ⚙️ Kurulum ve Yapılandırma
1. Bu repoyu klonlayın veya kendi üzerinize fork edin.
2. GitHub reponuzda **Settings > Secrets and variables > Actions** sekmesinden şu gizli değişkenleri (`Secrets`) tanımlayın:
   * `CANVAS_API_KEY`
   * `TELEGRAM_BOT_TOKEN`
   * `TELEGRAM_CHAT_ID`
3. `.github/workflows/bot.yml` dosyasındaki cron ayarını dilediğiniz zaman periyoduna göre özelleştirin.
