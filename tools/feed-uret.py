#!/usr/bin/env python3
"""RSS feed (feed.xml) üretir ve sayfalara RSS discovery link ekler.

Kullanım (depo kökünden):  python3 tools/feed-uret.py

İki iş yapar:
1. Ders sayfalarından feed.xml (RSS 2.0) üretir.
2. Tüm public sayfalara <link rel="alternate" type="application/rss+xml"> ekler
   (idempotent — mevcut satır varsa tekrar eklemez).
"""
import pathlib
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ehliyet.digital"
FEED_URL = f"{BASE}/feed.xml"
RSS_LINK = '<link rel="alternate" type="application/rss+xml" title="ehliyet.digital RSS" href="/feed.xml">'

KATEGORI_ADI = {
    "ilk-yardim": "İlk Yardım",
    "trafik-ve-cevre": "Trafik ve Çevre",
    "arac-teknigi": "Araç Tekniği",
    "trafik-adabi": "Trafik Adabı",
}


def metin(kalip, t, grup=1):
    m = re.search(kalip, t, re.S)
    return re.sub(r"<[^>]+>", "", m.group(grup)).strip() if m else None


def son_degisiklik(yol):
    try:
        c = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(yol)],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        if c:
            return c
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return datetime.fromtimestamp(yol.stat().st_mtime, tz=timezone.utc).isoformat()


# --- 1. feed.xml üret ---
ATOM_NS = "http://www.w3.org/2005/Atom"
ET.register_namespace("atom", ATOM_NS)

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "ehliyet.digital — Ehliyet Sınavı Ders Notları"
ET.SubElement(channel, "link").text = f"{BASE}/"
ET.SubElement(channel, "description").text = (
    "Ehliyet sınavına hazırlık: MEB MTSK müfredatına uygun ders notları, "
    "hap bilgiler ve deneme sınavları."
)
ET.SubElement(channel, "language").text = "tr"
ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime(
    "%a, %d %b %Y %H:%M:%S +0000"
)
ET.SubElement(channel, f"{{{ATOM_NS}}}link", attrib={
    "href": FEED_URL, "rel": "self", "type": "application/rss+xml"
})

sayac = 0
for p in sorted(ROOT.rglob("index.html")):
    parcalar = p.relative_to(ROOT).parts
    if len(parcalar) != 4 or parcalar[0] != "dersler":
        continue
    kategori = parcalar[1]
    if kategori not in KATEGORI_ADI:
        continue

    t = p.read_text(encoding="utf-8")
    baslik = metin(r"<h1[^>]*>(.*?)</h1>", t)
    aciklama = metin(r'<meta name="description" content="([^"]+)">', t)
    kanon = metin(r'<link rel="canonical" href="([^"]+)">', t)
    if not (baslik and aciklama and kanon):
        continue

    tarih = son_degisiklik(p)

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = baslik
    ET.SubElement(item, "link").text = kanon
    ET.SubElement(item, "description").text = aciklama
    ET.SubElement(item, "guid", isPermaLink="true").text = kanon
    ET.SubElement(item, "pubDate").text = tarih
    ET.SubElement(item, "category").text = KATEGORI_ADI[kategori]
    sayac += 1

ET.indent(rss, space="  ")
hedef = ROOT / "feed.xml"
hedef.write_bytes(
    b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(rss, encoding="utf-8")
)
print(f"{sayac} ders -> {hedef.relative_to(ROOT)}")

# --- 2. RSS discovery link ekle ---
eklenen = 0
for p in sorted(ROOT.rglob("index.html")):
    if any(x in p.relative_to(ROOT).parts for x in (".git", ".claude", "panel")):
        continue
    t = p.read_text(encoding="utf-8")
    if "application/rss+xml" in t:
        continue
    # </head>'den hemen önce ekle
    if "</head>" not in t:
        continue
    t = t.replace("</head>", f"{RSS_LINK}\n</head>", 1)
    p.write_text(t, encoding="utf-8")
    eklenen += 1

print(f"{eklenen} sayfaya RSS link eklendi")
