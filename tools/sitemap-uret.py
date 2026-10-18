#!/usr/bin/env python3
"""sitemap.xml'i site içindeki index.html dosyalarından üretir.

Kullanım (depo kökünden):  python3 tools/sitemap-uret.py

Yeni ders ya da sınav eklendiğinde tekrar çalıştırılır; sitemap elle
düzenlenmez. Panel sayfaları, noindex işaretli sayfalar ve canonical'ı başka adresi
gösteren sayfalar dışarıda bırakılır.
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
    (re.compile(r"^/(ehliyet-sinav-sorulari|deneme-sinavi)/$"), "0.9"),
    (re.compile(r"^/(dersler|hap-bilgiler)/$"), "0.8"),
    (re.compile(r"^/dersler/"), "0.7"),
    (re.compile(r"^/soru/"), "0.6"),
    (re.compile(r"^/hap-bilgiler/[^/]+/[^/]+/$"), "0.6"),  # tekil hap bilgi sayfaları
]
VARSAYILAN_ONCELIK = "0.5"

DEGISIM_SIKLIGI = [
    (re.compile(r"^/$"), "weekly"),
    (re.compile(r"^/(dersler|hap-bilgiler|ehliyet-sinav-sorulari|deneme-sinavi)/$"), "weekly"),
    (re.compile(r"^/dersler/"), "monthly"),
    (re.compile(r"^/hap-bilgiler/"), "monthly"),
]
VARSAYILAN_SIKLIK = "monthly"


def son_degisiklik(yol: pathlib.Path) -> str:
    """Dosyanın son commit tarihi; git yoksa dosya sistemi zamanına düşer."""
    try:
        cikti = subprocess.run(
            # Tarih guncelleme commit'leri ("chore: sitemap ...") sayilmaz: yalniz tarih
            # degistirdikleri icin sayilsalar her calismada tarihleri yeniden ileri iterlerdi.
            ["git", "log", "-1", "--invert-grep", "--grep=^chore:", "--format=%cs", "--", str(yol)],
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
        if ".git" in parcalar or ".claude" in parcalar or "panel" in parcalar or "mcp" in parcalar:
            continue
        metin = p.read_text(encoding="utf-8")
        if 'name="robots"' in metin and "noindex" in metin:
            continue
        dizin = p.relative_to(ROOT).parent.as_posix()
        yol = "/" if dizin == "." else f"/{dizin}/"
        # canonical'ı başka bir adresi gösteren sayfa (ör. başka sınavda tekrar
        # çıkmış sorunun kopyası) sitemap'e girmez; Google yalnız asıl adresi görür.
        kanon = re.search(r'<link rel="canonical" href="([^"]+)"', metin)
        if kanon and kanon.group(1) != BASE + yol:
            continue
        yield p, yol


NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
IMG_NS = "http://www.google.com/schemas/sitemap-image/1.1"
ET.register_namespace("", NS)
ET.register_namespace("image", IMG_NS)
kok = ET.Element(f"{{{NS}}}urlset")


def icerik_gorselleri(dosya):
    """Sayfa içeriğindeki görseller (soru görselleri, trafik işaretleri); logo ve OG hariç.
    Google Görseller'den gelen trafik için image sitemap'e yazılır."""
    metin = dosya.read_text(encoding="utf-8")
    govde = metin.split("<main", 1)[-1].split("</main>", 1)[0]
    gorulen = []
    for src in re.findall(r'<img[^>]+src="(/assets/img/[^"]+)"', govde):
        if src.startswith(("/assets/img/marka/", "/assets/img/og/")) or src in gorulen:
            continue
        gorulen.append(src)
    return gorulen[:1000]

sayac = 0
for dosya, yol in sayfalar():
    url = ET.SubElement(kok, f"{{{NS}}}url")
    ET.SubElement(url, f"{{{NS}}}loc").text = BASE + yol
    ET.SubElement(url, f"{{{NS}}}lastmod").text = son_degisiklik(dosya)
    ET.SubElement(url, f"{{{NS}}}changefreq").text = degisim_sikligi(yol)
    ET.SubElement(url, f"{{{NS}}}priority").text = oncelik(yol)
    for src in icerik_gorselleri(dosya):
        g = ET.SubElement(url, f"{{{IMG_NS}}}image")
        ET.SubElement(g, f"{{{IMG_NS}}}loc").text = BASE + src
    sayac += 1

# Statik kesfedilebilirlik dosyalari
for statik, onc in [("/feed.xml", "0.1"), ("/llms.txt", "0.1"), ("/llms-full.txt", "0.1")]:
    dosya = ROOT / statik.lstrip("/")
    if dosya.exists():
        url = ET.SubElement(kok, f"{{{NS}}}url")
        ET.SubElement(url, f"{{{NS}}}loc").text = BASE + statik
        ET.SubElement(url, f"{{{NS}}}lastmod").text = son_degisiklik(dosya)
        ET.SubElement(url, f"{{{NS}}}changefreq").text = "weekly"
        ET.SubElement(url, f"{{{NS}}}priority").text = onc
        sayac += 1

ET.indent(kok, space="  ")
hedef = ROOT / "sitemap.xml"
hedef.write_bytes(
    b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(kok, encoding="utf-8")
)
print(f"{sayac} URL yazildi -> {hedef.relative_to(ROOT)}")
