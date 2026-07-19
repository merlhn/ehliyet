#!/usr/bin/env python3
"""Giris gerektiren hicbir sayfanin indekslenmedigini dogrular.

Kullanim (depo kokunden):  python3 tools/index-kontrol.py
Cikis kodu 1 ise ihlal var; yayina alinmadan once duzeltilmeli.

Kural: kullanici giris yaptiktan sonra gordugu hicbir sayfa arama
sonuclarinda yer almaz. Uc katman birden saglanmali:

  1. sayfada  <meta name="robots" content="noindex">
  2. robots.txt icinde dizini Disallow
  3. sitemap.xml icinde adresi bulunmamali

Ucu de gerekli, ciddiye alinmali: robots.txt yalnizca taramayi engeller
indekslemeyi degil — sayfaya disaridan link verilirse Google adresi
yine listeleyebilir. Indekslemeyi durduran sey noindex etiketidir.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Sayfanin giris gerektirdigini gosteren isaretler. Yeni bir yetki mekanizmasi
# eklenirse buraya da eklenmeli, yoksa kontrol o sayfayi gozden kacirir.
KAPI_ISARETLERI = ("panel-kabuk.js", "kullaniciDinle")
KAPILI_DIZINLER = ("panel",)

ihlaller = []


def kapili_mi(yol: pathlib.Path, metin: str) -> bool:
    if any(d in yol.relative_to(ROOT).parts for d in KAPILI_DIZINLER):
        return True
    return any(isaret in metin for isaret in KAPI_ISARETLERI)


robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

kapili_sayfalar = []
for p in sorted(ROOT.rglob("index.html")):
    if ".git" in p.parts or ".claude" in p.parts:
        continue
    metin = p.read_text(encoding="utf-8")
    if not kapili_mi(p, metin):
        continue

    rel = p.relative_to(ROOT)
    kapili_sayfalar.append(rel)

    # 1. noindex etiketi
    if not re.search(r'<meta\s+name="robots"[^>]*noindex', metin):
        ihlaller.append(f"{rel}: noindex etiketi yok")

    # 2. sitemap'te yer almamali
    dizin = rel.parent.as_posix()
    url_yolu = "/" if dizin == "." else f"/{dizin}/"
    if f"<loc>https://ehliyet.digital{url_yolu}</loc>" in sitemap:
        ihlaller.append(f"{rel}: sitemap.xml icinde listelenmis")

# 3. robots.txt her kapili dizini engellemeli
for d in KAPILI_DIZINLER:
    if f"Disallow: /{d}/" not in robots:
        ihlaller.append(f"robots.txt: /{d}/ icin Disallow satiri yok")

print(f"giris gerektiren sayfa: {len(kapili_sayfalar)}")
for rel in kapili_sayfalar:
    print(f"  {rel}")

if ihlaller:
    print(f"\n{len(ihlaller)} IHLAL:", file=sys.stderr)
    for i in ihlaller:
        print(f"  - {i}", file=sys.stderr)
    sys.exit(1)

print("\nsorun yok: kapili sayfalarin tamami indekslemeye kapali.")
