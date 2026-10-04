#!/usr/bin/env python3
"""Tüm public sayfalara header'ın üstünde "ücretsiz deneme sınavı" banner'ı ekler.

Banner doğrudan Sınav 1'i başlatır (/deneme-sinavi/?basla=1); tıklama GA4'e
banner_click olarak gider. /deneme-sinavi/ (banner kendi sayfasına çıkar) ve
/panel/ (girişli alan) hariç tutulur.

İdempotent: önceki banner ve stili silinip yeniden eklenir. Üreticiler sayfaları
banner'sız yazar ya da başka sayfanın header'ını kopyalar; bu yüzden zincirin EN
SONUNDA çalışır:  üreticiler → feed-uret → schema-uret → banner-ekle

Kullanım (depo kökünden):  python3 tools/banner-ekle.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HARIC = (".git", ".claude", "node_modules", "panel", "tools", "mcp", "deneme-sinavi")

CSS = ('<style id="ust-banner-css">'
       '.ust-banner{display:flex;align-items:center;justify-content:center;gap:10px;min-height:40px;padding:8px 16px;'
       'background:#08090a;color:#fff;font-size:13.5px;line-height:1.35;text-decoration:none;text-align:center}'
       '.ust-banner:hover b{text-decoration:underline}'
       '.ust-banner-rozet{background:#16a34a;border-radius:999px;padding:2px 8px;font-size:11.5px;font-weight:600;letter-spacing:.02em;flex-shrink:0}'
       '.ust-banner b{font-weight:600;white-space:nowrap}'
       '.ust-banner-kisa{display:none}'
       '@media(max-width:640px){.ust-banner{font-size:12.5px;gap:8px;padding:8px 12px}.ust-banner-uzun{display:none}.ust-banner-kisa{display:inline}}'
       '</style>')

BANNER = ('<!-- ust-banner -->\n'
          '<a class="ust-banner" href="/deneme-sinavi/?basla=1" '
          'onclick="typeof gtag===\'function\'&&gtag(\'event\',\'banner_click\',{sayfa:location.pathname})">'
          '<span class="ust-banner-rozet">Ücretsiz</span>'
          '<span class="ust-banner-uzun">Ehliyet deneme sınavı: 50 soru, 45 dakika, gerçek sınav formatı.</span>'
          '<span class="ust-banner-kisa">50 soruluk deneme sınavı.</span>'
          '<b>Hemen çöz →</b></a>\n'
          '<!-- /ust-banner -->\n')

ESKI_CSS = re.compile(r'<style id="ust-banner-css">.*?</style>\n?', re.S)
ESKI_BANNER = re.compile(r'[ \t]*<!-- ust-banner -->.*?<!-- /ust-banner -->\n?', re.S)
BODY = re.compile(r'<body[^>]*>\n?')

eklenen = temizlenen = 0
for p in sorted(ROOT.rglob("*.html")):
    if any(x in p.relative_to(ROOT).parts for x in HARIC):
        continue
    t = p.read_text(encoding="utf-8")
    yeni = ESKI_BANNER.sub("", ESKI_CSS.sub("", t))
    if "<header" in yeni and "</head>" in yeni and BODY.search(yeni):
        yeni = yeni.replace("</head>", CSS + "\n</head>", 1)
        yeni = BODY.sub(lambda m: m.group(0) + BANNER, yeni, count=1)
        eklenen += 1
    if yeni != t:
        p.write_text(yeni, encoding="utf-8")

# /deneme-sinavi/ header'ı ehliyet-sinav-sorulari'dan kopyalar; kopyalanan banner silinir.
for p in (ROOT / "deneme-sinavi").rglob("*.html"):
    t = p.read_text(encoding="utf-8")
    yeni = ESKI_BANNER.sub("", ESKI_CSS.sub("", t))
    if yeni != t:
        p.write_text(yeni, encoding="utf-8"); temizlenen += 1

print(f"{eklenen} sayfada banner var; deneme-sinavi'dan {temizlenen} kopya temizlendi")
