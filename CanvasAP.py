import time
import requests
from canvasapi import Canvas
import re
import html

# --- AYARLAR ---
CANVAS_API_URL = "https://estuoys.eskisehir.edu.tr"
CANVAS_API_KEY = "rpt69SUbgpfHvAsrXH8esmArt0LgC5BHgcSg0f5c85xHbuczcHaKMJCuBbcc4HPZ"

TELEGRAM_BOT_TOKEN = "8997569775:AAH6eBTtLsOLRywBm4gpR4yr4E1zsUFVWSE"
TELEGRAM_CHAT_ID = "1082763849" # Sadece rakamlar

# Daha önce gönderilen duyuruların ID'lerini hafızada tutmak için küme (set)
gonderilen_duyurular = set()

def html_temizle(ham_metin):
    if not ham_metin:
        return ""
    metin = html.unescape(ham_metin)
    metin = metin.replace('<br>', '\n').replace('<br/>', '\n').replace('</p>', '\n\n')
    return re.sub(re.compile('<.*?>'), '', metin).strip()

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    parametreler = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj
    }
    try:
        cevap = requests.post(url, json=parametreler)
        if cevap.status_code == 200:
            print("Telegram'a yeni duyuru bildirimi gönderildi!")
        else:
            print(f"Mesaj gönderilemedi. Hata Kodu: {cevap.status_code}, Detay: {cevap.text}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# --- ANA PROGRAM ---
import os

canvas = Canvas(CANVAS_API_URL, CANVAS_API_KEY)
user = canvas.get_current_user()

print(f"Bot aktif! {user.name} için duyurular kontrol ediliyor...\n")

# Botun gönderdiği duyuruları hatırlaması için txt dosyası kullanıyoruz
DOSYA_ADI = "gonderilen_duyurular.txt"
gonderilen_duyurular = set()

# Dosya varsa içindeki eski ID'leri okuyup listeye ekle
if os.path.exists(DOSYA_ADI):
    with open(DOSYA_ADI, "r") as dosya:
        for satir in dosya:
            if satir.strip().isdigit():
                gonderilen_duyurular.add(int(satir.strip()))

try:
    courses = user.get_courses(enrollment_state="active")
    for course in courses:
        try:
            announcements = list(canvas.get_announcements(context_codes=[f"course_{course.id}"]))
            
            # Duyuruları eskiden yeniye sıralayalım
            announcements.reverse()
            
            for announcement in announcements:
                # Daha önce gönderilmediyse (yani listede yoksa):
                if announcement.id not in gonderilen_duyurular:
                    temiz_icerik = html_temizle(announcement.message)

                    mesaj = f"🔔 **YENİ CANVAS DUYURUSU**\n\n"
                    mesaj += f"📚 **Ders:** {course.name}\n"
                    mesaj += f"📌 **Başlık:** {announcement.title}\n\n"
                    mesaj += f"{temiz_icerik}"

                    # Telegram'a gönder
                    telegram_mesaj_gonder(mesaj)

                    # Listeye ekle ve txt dosyasına kalıcı olarak yaz
                    gonderilen_duyurular.add(announcement.id)
                    with open(DOSYA_ADI, "a") as dosya:
                        dosya.write(f"{announcement.id}\n")
                        
        except Exception:
            continue

except Exception as e:
    print(f"Kontrol sırasında hata oluştu: {e}")

print("\nKontrol tamamlandı. Bot kapanıyor (GitHub Actions zamanı gelince tekrar başlatacak).")

