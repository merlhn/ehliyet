#!/usr/bin/env python3
"""og-image.png (1200x630) uretir — WhatsApp, Facebook, LinkedIn onizlemesi.

Kullanim (depo kokunden):  python3 tools/og-gorsel-uret.py
Gereksinim:                python3 -m pip install Pillow

Marka dili siteyle ayni: beyaz zemin, neredeyse siyah metin (#08090a), gri
ikincil metin (#6a6f76). Site Inter kullaniyor; sistemde Inter olmadigi icin
en yakin karsiligi olan SF Pro (SFNS.ttf) ile uretiliyor.

Metin 80px kenar boslugunun icinde tutuluyor: WhatsApp ve bazi istemciler
onizlemeyi kirpabiliyor, kritik icerik kenara yaslanirsa kesiliyor.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = "/System/Library/Fonts/SFNS.ttf"
EN, BOY = 1200, 630
PAY = 80

FG = (8, 9, 10)
GRI = (106, 111, 118)
CIZGI = (236, 236, 236)


def yazi(boyut, agirlik="Regular"):
    f = ImageFont.truetype(FONT, boyut)
    try:
        f.set_variation_by_name(agirlik)
    except Exception:
        pass          # degisken font desteklenmiyorsa varsayilan agirlikla devam
    return f


tuval = Image.new("RGB", (EN, BOY), (255, 255, 255))
d = ImageDraw.Draw(tuval)

# --- Ust: logo isareti + kelime markasi ---
logo = Image.open(ROOT / "assets/img/marka/logo.png").convert("RGBA")
logo = logo.crop(logo.split()[3].getbbox())
h = 52
logo = logo.resize((int(logo.width * h / logo.height), h), Image.LANCZOS)
tuval.paste(logo, (PAY, PAY), logo)

f_marka = yazi(30, "Medium")
d.text((PAY + logo.width + 20, PAY + h // 2), "ehliyet.digital",
       font=f_marka, fill=FG, anchor="lm")

# --- Baslik ---
f_baslik = yazi(76, "Bold")
y = 236
for satir in ("Ehliyet sınavına", "ücretsiz hazırlan"):
    d.text((PAY, y), satir, font=f_baslik, fill=FG)
    y += 92

# --- Alt metin ---
f_alt = yazi(30, "Regular")
y = 442
for satir in ("Gerçek MTSK e-sınav formatında 50 soruluk deneme testleri,",
              "çözümlü cevaplar ve 4 derste 43 konu anlatımı."):
    d.text((PAY, y), satir, font=f_alt, fill=GRI)
    y += 44

# --- Alt ayrac ve etiket ---
d.line([(PAY, BOY - 96), (EN - PAY, BOY - 96)], fill=CIZGI, width=2)
f_etiket = yazi(26, "Medium")
# Buradaki ifadeler sitenin kendi metinlerinden dogrulanabilir olmali.
# "Uyelik gerekmez" yazilamaz: deneme sinavi /panel/ altinda ve giris istiyor.
d.text((PAY, BOY - 58), "Ücretsiz  ·  Çözümlü cevaplar  ·  Konu bazlı analiz",
       font=f_etiket, fill=GRI)

tuval.save(ROOT / "og-image.png", optimize=True)
kb = (ROOT / "og-image.png").stat().st_size / 1024
print(f"uretildi: og-image.png  {EN}x{BOY}  {kb:.0f} KB")
