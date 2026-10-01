#!/usr/bin/env python3
"""Bing Site Scan'in yakaladigi HTML hatalarini yayindan once yakalar.

Kullanim (depo kokunden):  python3 tools/html-kontrol.py
Cikis kodu 1 ise hata var; yayina alinmadan once duzeltilmeli.

Hatalar:
  1. Etiket ozniteliginde tipografik tirnak:  href=”/dersler/…”
     Tarayici ve tarayici botlari bunu tirnaksiz deger sayar; tirnak isaretleri
     adresin parcasi olur ve link 404'e gider. Kaynagi metin editorunden ya da
     modelden kopyalanan ders notlaridir.
  2. alt'i olmayan ya da bos olan <img>.
  3. 70 karakterden uzun <title> — Bing "Title too long" esigi. Marka eki
     (" | ehliyet.digital") sigmiyorsa atilir; ureticilerde sayfa_basligi().
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATLA = (".claude", ".git", "node_modules")
BASLIK_SINIRI = 70

TIRNAK = re.compile(r'<[a-zA-Z][^<>]*\s[a-zA-Z-]+=[”“‘’][^<>]*>')
IMG = re.compile(r"<img\b[^>]*>", re.I)
ALT = re.compile(r'\salt\s*=\s*"([^"]*)"', re.I)
TITLE = re.compile(r"<title>(.*?)</title>", re.S)

hatalar = []

for yol in sorted(ROOT.rglob("*.html")):
    rel = yol.relative_to(ROOT)
    if any(p in ATLA for p in rel.parts):
        continue
    metin = yol.read_text(encoding="utf-8")

    for m in TIRNAK.finditer(metin):
        hatalar.append(f"{rel}: tipografik tirnakli oznitelik: {m.group(0)[:100]}")

    for m in IMG.finditer(metin):
        etiket = m.group(0)
        alt = ALT.search(etiket)
        if not alt or not alt.group(1).strip():
            hatalar.append(f"{rel}: alt'i eksik ya da bos <img>: {etiket[:100]}")

    t = TITLE.search(metin)
    if t:
        baslik = html.unescape(t.group(1).strip())
        if len(baslik) > BASLIK_SINIRI:
            hatalar.append(f"{rel}: <title> {len(baslik)} karakter (sinir {BASLIK_SINIRI}): {baslik}")

for h in hatalar:
    print("HATA  ", h)
print(f"{len(hatalar)} hata")
sys.exit(1 if hatalar else 0)
