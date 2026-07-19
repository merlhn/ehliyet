#!/usr/bin/env python3
"""Favicon setini assets/img/marka/logo.png dosyasindan uretir.

Kullanim (depo kokunden):  python3 tools/favicon-uret.py
Gereksinim:                python3 -m pip install Pillow

Logo degisirse tekrar calistirilir; uretilen dosyalar elle duzenlenmez.

Tasarim kararlari:
- Logonun seffaf kenar boslugu kirpilir. Kaynak 500x500 tuvalde 434x320'lik
  yatay bir icerik tasiyor; kirpilmazsa favicon'un ucte biri bos kalir.
- Zemin beyaz. Logo neredeyse siyah (#241E20) ve seffaf zeminde geliyor;
  oldugu gibi birakilsa tarayicinin koyu tema sekme seridinde kaybolurdu.
  Beyaz dosemenin kendisi kontrast sagliyor, ikon her sekme renginde okunuyor.
- apple-touch-icon kosesiz ve tamamen opak uretilir: iOS kendi maskesini
  uyguluyor, onceden yuvarlatilirsa koseler iki kez kirpilmis gorunuyor.
"""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
KAYNAK = ROOT / "assets/img/marka/logo.png"
ZEMIN = (255, 255, 255, 255)
PAY = 0.16        # kenar boslugu orani
YUVARLAK = 0.22   # kose yaricapi orani

src = Image.open(KAYNAK).convert("RGBA")
logo = src.crop(src.split()[3].getbbox())


def dose(boyut, yuvarlak=YUVARLAK, opak=False):
    """Logoyu belirtilen boyutta zemine ortalar."""
    tuval = Image.new("RGBA", (boyut, boyut), ZEMIN if opak else (0, 0, 0, 0))
    if not opak:
        maske = Image.new("L", (boyut, boyut), 0)
        ImageDraw.Draw(maske).rounded_rectangle(
            [0, 0, boyut - 1, boyut - 1], radius=int(boyut * yuvarlak), fill=255)
        tuval.paste(Image.new("RGBA", (boyut, boyut), ZEMIN), (0, 0), maske)

    ic = int(boyut * (1 - 2 * PAY))
    o = min(ic / logo.width, ic / logo.height)
    l = logo.resize((max(1, int(logo.width * o)), max(1, int(logo.height * o))),
                    Image.LANCZOS)
    tuval.paste(l, ((boyut - l.width) // 2, (boyut - l.height) // 2), l)
    return tuval


# Coklu boyutlu .ico — tarayici sekme, yer imi ve gecmis icin farkli boyut secer.
dose(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# iOS ana ekran kisayolu: kosesiz, seffaflik yok. RGB'ye duzlestiriliyor —
# PIL'in maskeli yapistirmasi yumusatilmis kenar piksellerinde hedefin alfasini
# da dusuruyor; RGBA birakilsa iOS bunu koyu bir kenar halkasi olarak basiyor.
dose(180, opak=True).convert("RGB").save(ROOT / "apple-touch-icon.png")

# Web app manifest ikonlari.
for boyut in (192, 512):
    dose(boyut).save(ROOT / f"icon-{boyut}.png")

print("uretildi: favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png")
