#!/usr/bin/env python3
"""Sayfalara schema.org (JSON-LD) yapisal verisini gomer.

Kullanim (depo kokunden):  python3 tools/schema-uret.py

Idempotent: mevcut blok isaretciler arasindan silinip yeniden yazilir, tekrar
tekrar calistirilabilir. Ders ya da sinav eklendikten sonra calistirilir.

Veriler sayfanin kendisinden okunur (h1, meta description, canonical) — ikinci
bir kaynak tutulmaz, boylece sayfa ile yapisal veri ayrisamaz.

Kapsam disi biraktiklarimiz:
- FAQPage: Google 2023'te SSS zengin sonuclarini dar bir otorite grubuna
  kisitladi. Ders notlarindaki h2 basliklari soru gibi gorunse de gercek bir
  SSS bloguu degil; yanlis isaretleme manuel eylem riski tasiyor.
- SearchAction: site ici arama tamamen istemci tarafinda (fuse.js), sonuc
  URL'i uretmiyor. Google'in istedigi "arama sonucu adresi" yok.
- Ders seviyesi kirinti (ornegin /dersler/ilk-yardim/): boyle bir sayfa yok,
  404 doner. Ders adi articleSection olarak isaretleniyor.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ehliyet.digital"
GORSEL = f"{BASE}/og-image.png"
BAS = "<!-- schema.org — tools/schema-uret.py tarafından üretilir, elle düzenlenmez -->"
SON = "<!-- /schema.org -->"

GORSEL_OBJ = {
    "@type": "ImageObject",
    "url": GORSEL,
    "width": 1200,
    "height": 630,
}
LOGO_OBJ = {
    "@type": "ImageObject",
    "url": f"{BASE}/icon-512.png",
    "width": 512,
    "height": 512,
}
YAYINCI = {
    "@type": "Organization",
    "@id": f"{BASE}/#organization",
    "name": "ehliyet.digital",
    "alternateName": ["Ehliyet Digital", "ehliyet digital"],
    "url": f"{BASE}/",
    "logo": LOGO_OBJ,
    "description": "Ehliyet (sürücü belgesi) sınavına hazırlık için ücretsiz, reklamsız ve bağımsız çalışma platformu.",
    "foundingDate": "2026",
    "areaServed": "TR",
    "knowsAbout": [
        "ehliyet sınavı", "MTSK e-sınav", "sürücü belgesi",
        "trafik ve çevre bilgisi", "ilk yardım", "araç tekniği", "trafik adabı",
    ],
}
YAYINCI_EGITIM = {
    **YAYINCI,
    "@type": ["Organization", "EducationalOrganization"],
}
SITE = {"@type": "WebSite", "name": "ehliyet.digital", "url": f"{BASE}/"}

# Ders kategorileri — Course schema icin
KATEGORI_ADI = {
    "ilk-yardim": "İlk Yardım",
    "trafik-ve-cevre": "Trafik ve Çevre",
    "arac-teknigi": "Araç Tekniği (Motor)",
    "trafik-adabi": "Trafik Adabı",
}


def son_degisiklik(yol):
    try:
        c = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(yol)],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        if c:
            return c
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    import datetime
    return datetime.datetime.fromtimestamp(yol.stat().st_mtime).astimezone().isoformat()


def kirinti(ogeler):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": ad,
             **({"item": url} if url else {})}
            for i, (ad, url) in enumerate(ogeler, 1)
        ],
    }


def metin(kalip, t, grup=1):
    m = re.search(kalip, t, re.S)
    return re.sub(r"<[^>]+>", "", m.group(grup)).strip() if m else None


sayac, hata = {}, []

for p in sorted(ROOT.rglob("index.html")):
    if any(x in p.relative_to(ROOT).parts for x in (".git", ".claude", "panel")):
        continue
    t = p.read_text(encoding="utf-8")

    # Onceki blogu temizle (idempotency)
    t = re.sub(re.escape(BAS) + r".*?" + re.escape(SON) + r"\n?", "", t, flags=re.S)

    kanon = metin(r'<link rel="canonical" href="([^"]+)">', t)
    aciklama = metin(r'<meta name="description" content="([^"]+)">', t)
    h1 = metin(r"<h1[^>]*>(.*?)</h1>", t)
    if not (kanon and aciklama and h1):
        hata.append(f"{p.relative_to(ROOT)}: canonical/description/h1 eksik")
        continue

    dizin = p.parent.relative_to(ROOT).as_posix()
    ders_notu = bool(re.match(r"^dersler/[^/]+/[^/]+$", dizin))

    if dizin == ".":
        graf = [
            {**SITE, "description": aciklama, "inLanguage": "tr-TR",
             "publisher": YAYINCI_EGITIM},
            {**YAYINCI_EGITIM, "description": aciklama},
        ]
        tur = "anasayfa"

    elif ders_notu:
        ders = metin(r'<span class="k">Ders</span>\s*:\s*<b>(.*?)</b>', t) or ""
        tarih_yay = metin(r'<meta property="article:published_time" content="([^"]+)">', t)
        tarih_mod = son_degisiklik(p)
        graf = [
            {
                "@type": ["Article", "LearningResource"],
                "headline": h1,
                "description": aciklama,
                "url": kanon,
                "image": GORSEL_OBJ,
                "inLanguage": "tr-TR",
                "articleSection": ders,
                "learningResourceType": "ders notu",
                "educationalLevel": "B sınıfı ehliyet",
                "teaches": h1,
                **({"datePublished": tarih_yay} if tarih_yay else {}),
                "dateModified": tarih_mod,
                "author": YAYINCI,
                "publisher": YAYINCI,
                "isPartOf": SITE,
            },
            kirinti([("Ana Sayfa", f"{BASE}/"),
                     ("Dersler", f"{BASE}/dersler/"),
                     (h1, kanon)]),
        ]
        tur = "ders notu"

    elif re.match(r"^dersler/[^/]+$", dizin) and dizin.split("/")[1] in KATEGORI_ADI:
        # Kategorideki ders sayisini sayfa iceriginden cikar
        ders_sayisi = len(re.findall(r'<a[^>]+class="[^"]*lesson[^"]*"', t))
        kurs = {
            "@type": "Course",
            "name": h1,
            "description": aciklama,
            "url": kanon,
            "inLanguage": "tr-TR",
            "provider": YAYINCI,
            "isAccessibleForFree": True,
            "educationalLevel": "B sınıfı ehliyet",
            "isPartOf": SITE,
        }
        if ders_sayisi:
            kurs["hasCourseInstance"] = {
                "@type": "CourseInstance",
                "courseMode": "online",
                "courseWorkload": f"{ders_sayisi} konu",
            }
        graf = [
            kurs,
            kirinti([("Ana Sayfa", f"{BASE}/"),
                     ("Dersler", f"{BASE}/dersler/"),
                     (h1, kanon)]),
        ]
        tur = "ders kategorisi"

    elif re.match(r"^hap-bilgiler/[^/]+$", dizin):
        graf = [
            {"@type": "WebPage",
             "name": h1, "description": aciklama, "url": kanon,
             "inLanguage": "tr-TR", "isPartOf": SITE, "publisher": YAYINCI},
            kirinti([("Ana Sayfa", f"{BASE}/"),
                     ("Hap Bilgiler", f"{BASE}/hap-bilgiler/"),
                     (h1, kanon)]),
        ]
        tur = "hap bilgi"

    elif dizin == "hakkinda":
        graf = [
            {"@type": "AboutPage",
             "name": h1, "description": aciklama, "url": kanon,
             "inLanguage": "tr-TR", "isPartOf": SITE, "publisher": YAYINCI},
            {"@type": "Person",
             "name": "Ömer İlhan",
             "jobTitle": "Kurucu ve İçerik Editörü",
             "worksFor": YAYINCI},
            kirinti([("Ana Sayfa", f"{BASE}/"), (h1, kanon)]),
        ]
        tur = "hakkinda"

    else:
        graf = [
            {"@type": "CollectionPage" if dizin in ("dersler", "deneme-sinavlari", "hap-bilgiler") else "WebPage",
             "name": h1, "description": aciklama, "url": kanon,
             "inLanguage": "tr-TR", "isPartOf": SITE, "publisher": YAYINCI},
            kirinti([("Ana Sayfa", f"{BASE}/"), (h1, kanon)]),
        ]
        tur = "hub/kurumsal"

    veri = json.dumps({"@context": "https://schema.org", "@graph": graf},
                      ensure_ascii=False, indent=2)
    if "</script" in veri:
        hata.append(f"{p.relative_to(ROOT)}: icerikte </script gecti")
        continue

    blok = f'{BAS}\n<script type="application/ld+json">\n{veri}\n</script>\n{SON}\n'
    i = t.index("</head>")
    p.write_text(t[:i] + blok + t[i:], encoding="utf-8")
    sayac[tur] = sayac.get(tur, 0) + 1

for k, v in sorted(sayac.items()):
    print(f"{k:<14}: {v}")
print(f"{'toplam':<14}: {sum(sayac.values())}")
if hata:
    print("\nHATA:", file=sys.stderr)
    for h in hata:
        print("  -", h, file=sys.stderr)
    sys.exit(1)
