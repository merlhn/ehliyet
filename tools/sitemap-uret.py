#!/usr/bin/env python3
"""sitemap.xml'i site içindeki index.html dosyalarından üretir.

Kullanım (depo kökünden):  python3 tools/sitemap-uret.py

Yeni ders ya da sınav eklendiğinde tekrar çalıştırılır; sitemap elle
düzenlenmez. Panel sayfaları ve noindex işaretli sayfalar dışarıda bırakılır.
"""
import pathlib
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ehliyet.digital"

# Ana sayfa ve hub sayfaları daha sık taranmalı; ders notları nadiren değişir.
ONCELIK = [
    (re.compile(r"^/$"), "1.0"),
    (re.compile(r"^/(dersler|deneme-sinavlari)/$"), "0.9"),
    (re.compile(r"^/deneme-sinavlari/"), "0.8"),
    (re.compile(r"^/dersler/"), "0.7"),
]
VARSAYILAN_ONCELIK = "0.5"

DEGISIM_SIKLIGI = [
    (re.compile(r"^/$"), "weekly"),
    (re.compile(r"^/(dersler|hap-bilgiler)/$"), "weekly"),
    (re.compile(r"^/dersler/"), "monthly"),
    (re.compile(r"^/hap-bilgiler/"), "monthly"),
]
VARSAYILAN_SIKLIK = "monthly"


def son_degisiklik(yol: pathlib.Path) -> str:
    """Dosyanın son commit tarihi; git yoksa dosya sistemi zamanına düşer."""
    try:
        cikti = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(yol)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if cikti:
            return cikti
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    import datetime
    return datetime.date.fromtimestamp(yol.stat().st_mtime).isoformat()


def oncelik(url_yolu: str) -> str:
    for kalip, deger in ONCELIK:
        if kalip.search(url_yolu):
            return deger
    return VARSAYILAN_ONCELIK


def degisim_sikligi(url_yolu: str) -> str:
    for kalip, deger in DEGISIM_SIKLIGI:
        if kalip.search(url_yolu):
            return deger
    return VARSAYILAN_SIKLIK


def sayfalar():
    for p in sorted(ROOT.rglob("index.html")):
        parcalar = p.relative_to(ROOT).parts
        if ".git" in parcalar or ".claude" in parcalar or "panel" in parcalar:
            continue
        if 'name="robots"' in p.read_text(encoding="utf-8") and "noindex" in p.read_text(encoding="utf-8"):
            continue
        dizin = p.relative_to(ROOT).parent.as_posix()
        yield p, "/" if dizin == "." else f"/{dizin}/"


NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
kok = ET.Element(f"{{{NS}}}urlset")

sayac = 0
for dosya, yol in sayfalar():
    url = ET.SubElement(kok, f"{{{NS}}}url")
    ET.SubElement(url, f"{{{NS}}}loc").text = BASE + yol
    ET.SubElement(url, f"{{{NS}}}lastmod").text = son_degisiklik(dosya)
    ET.SubElement(url, f"{{{NS}}}changefreq").text = degisim_sikligi(yol)
    ET.SubElement(url, f"{{{NS}}}priority").text = oncelik(yol)
    sayac += 1

ET.indent(kok, space="  ")
hedef = ROOT / "sitemap.xml"
hedef.write_bytes(
    b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(kok, encoding="utf-8")
)
print(f"{sayac} URL yazildi -> {hedef.relative_to(ROOT)}")
