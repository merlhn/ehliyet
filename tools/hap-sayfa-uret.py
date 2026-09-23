#!/usr/bin/env python3
"""
Hap bilgi sayfası üretici — 80 hap bilginin her birini
/hap-bilgiler/{kategori}/{slug}/index.html olarak üretir ve kategori
sayfalarındaki hap numaralarını bu sayfalara link yapar.

Çalıştırmak için: python3 tools/hap-sayfa-uret.py

Kaynaklar:
- tools/hap-uret.py  → DERSLER (hap bilgi HTML'i, grup başlıkları, slug kuralı)
- mcp/data/quick-facts.json → düz metin doğrulaması
- mcp/data/lesson-summaries.json → en alakalı ders notu (kelime örtüşmesi)

Idempotent: sayfalar her çalıştırmada yeniden yazılır, artık slug klasörleri
silinir, kategori sayfalarındaki linkler yerinde güncellenir.
"""

import os
import re
import html
import json
import shutil
import pathlib
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAP_DIR = os.path.join(ROOT, "hap-bilgiler")
DATA_DIR = os.path.join(ROOT, "mcp", "data")
# İsteğe bağlı ayrıntılı içerik: tools/hap-detay/{slug}.html
# İlk satırlarda <!-- baslik: ... --> ve <!-- aciklama: ... --> yorumları varsa
# sayfa başlığı ve meta açıklaması olarak kullanılır; kalan HTML "detay" bölümüdür.
DETAY_DIR = os.path.join(ROOT, "tools", "hap-detay")
SORU_DIR = os.path.join(ROOT, "soru")
DOMAIN = "https://ehliyet.digital"
YAYIN_TARIHI = "2026-08-24"

# hap-uret.py'den DERSLER, slug ve yardımcıları al (dosya adı tireli, import edilemez)
_spec = importlib.util.spec_from_file_location("hap_uret", os.path.join(ROOT, "tools", "hap-uret.py"))
hap_uret = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hap_uret)
DERSLER = hap_uret.DERSLER
hap_listesi = hap_uret.hap_listesi

SECTION_URL = {
    "İlk Yardım": "/dersler/ilk-yardim/",
    "Trafik ve Çevre": "/dersler/trafik-ve-cevre/",
    "Araç Tekniği": "/dersler/arac-teknigi/",
    "Trafik Adabı": "/dersler/trafik-adabi/",
}

# Eşleme eşiği: en az bu kadar farklı kök örtüşmezse ders yerine hub'a bağlanır.
MIN_ORTUSME = 2

# Çok sık geçen, ayırt edici olmayan kelimeler
DURAK = {
    "için", "gibi", "olan", "olarak", "veya", "ancak", "değil", "değildir", "yapılır",
    "yapılmaz", "olur", "olmaz", "ile", "bir", "her", "daha", "kadar", "sonra", "önce",
    "yoksa", "varsa", "diğer", "şekilde", "durumda", "sayılır", "edilir", "verilir",
    "ise", "bunlar", "bunun", "buna", "yani", "kendi", "yalnızca", "sadece", "sürücü",
    "sürücünün", "araç", "aracın", "araçlar", "sınav", "sınavda", "trafik", "trafikte",
}


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def esc(text):
    return html.escape(text, quote=True)


def truncate(text, max_len):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 1].rsplit(" ", 1)[0] + "..."


def tr_lower(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def kokler(text):
    """Basit, deterministik kök kümesi: küçük harf, noktalama yok, ≥5 harf, ilk 6 harf."""
    t = tr_lower(re.sub(r"<[^>]+>", "", text))
    t = re.sub(r"[^\w\s]", " ", t)
    out = set()
    for w in t.split():
        if len(w) < 5 or w in DURAK or w.isdigit():
            continue
        out.add(w[:6])
    return out


# ---------------------------------------------------------------------------
# Ders eşleme
# ---------------------------------------------------------------------------

import math

def dersleri_yukle():
    with open(os.path.join(DATA_DIR, "lesson-summaries.json"), encoding="utf-8") as f:
        dersler = json.load(f)
    for d in dersler:
        d["_ad_kok"] = kokler(d["lesson"])
        d["_kok"] = d["_ad_kok"] | kokler(" ".join(d["facts"]))
        d["_fact_kok"] = [kokler(x) for x in d["facts"]]
    # IDF: tüm derslerde yaygın kökler (ör. "sürücü") az, nadir kökler çok sayılır
    df = {}
    for d in dersler:
        for k in d["_kok"]:
            df[k] = df.get(k, 0) + 1
    n = len(dersler)
    for d in dersler:
        d["_idf"] = {k: math.log(n / df[k]) for k in d["_kok"]}
    return dersler


def puan(hk, d):
    """Ağırlıklı örtüşme; ders adındaki kökler ekstra sayılır."""
    ortak = hk & d["_kok"]
    p = sum(d["_idf"][k] for k in ortak)
    p += 2.0 * len(ortak & d["_ad_kok"])
    return p, len(ortak)


# Eşleme eşiği (ağırlıklı puan). Altında kalanlar kategori hub'ına bağlanır.
MIN_PUAN = 8.0


def en_iyi_ders(hap_duz, section, dersler):
    """Aynı bölümdeki dersler arasında en çok örtüşen dersi döndürür; eşik altıysa None."""
    hk = kokler(hap_duz)
    adaylar = []
    for d in dersler:
        if d["section"] != section:
            continue
        p, adet = puan(hk, d)
        if adet >= MIN_ORTUSME and p >= MIN_PUAN:
            adaylar.append((p, d["lesson"], d))
    if not adaylar:
        return None
    adaylar.sort(key=lambda x: (-x[0], x[1]))
    return adaylar[0][2]


def ilgili_satirlar(hap_duz, ders, adet=2):
    """Eşlenen dersin atomik satırlarından hap bilgiyle en çok örtüşen 1–2 satır (≥2 ortak kök)."""
    hk = kokler(hap_duz)
    puanli = []
    for fact, fk in zip(ders["facts"], ders["_fact_kok"]):
        ortak = hk & fk
        if len(ortak) >= 2 and fact.strip() != hap_duz.strip():
            puanli.append((sum(ders["_idf"].get(k, 0) for k in ortak), fact))
    puanli.sort(key=lambda x: (-x[0], x[1]))
    return [f for _, f in puanli[:adet]]


# ---------------------------------------------------------------------------
# Sayfa
# ---------------------------------------------------------------------------

def detay_oku(slug):
    yol = os.path.join(DETAY_DIR, f"{slug}.html")
    if not os.path.exists(yol):
        return None
    metin = open(yol, encoding="utf-8").read()
    sonuc = {"baslik": None, "aciklama": None}
    for alan in ("baslik", "aciklama"):
        m = re.search(r"<!--\s*" + alan + r":\s*(.*?)\s*-->\n?", metin)
        if m:
            sonuc[alan] = m.group(1).strip()
            metin = metin.replace(m.group(0), "", 1)
    sonuc["html"] = metin.strip("\n")
    return sonuc


_SORULAR = None

def sorulari_yukle():
    """Soru sayfalarından (bölüm, slug, başlık, kökler); ikinci bir liste tutulmaz."""
    global _SORULAR
    if _SORULAR is not None:
        return _SORULAR
    _SORULAR = []
    if os.path.isdir(SORU_DIR):
        for ad in sorted(os.listdir(SORU_DIR)):
            yol = os.path.join(SORU_DIR, ad, "index.html")
            if not os.path.exists(yol):
                continue
            t = open(yol, encoding="utf-8").read()
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            bolum = re.search(r"Bu soru <b>([^<]+)</b> konusuna aittir", t)
            if not h1 or not bolum:
                continue
            baslik = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<br\s*/?>", " ", h1.group(1))))).strip()
            _SORULAR.append((bolum.group(1), ad, baslik, kokler(baslik)))
    return _SORULAR


_SORU_DF = None

def soru_df(section):
    """Bölümdeki soru başlıklarında her kökün kaç soruda geçtiği (doküman sıklığı)."""
    global _SORU_DF
    if _SORU_DF is None:
        _SORU_DF = {}
        for bolum, _slug, _baslik, sk in sorulari_yukle():
            df = _SORU_DF.setdefault(bolum, {"_n": 0})
            df["_n"] += 1
            for k in sk:
                df[k] = df.get(k, 0) + 1
    return _SORU_DF.get(section, {"_n": 0})


def ilgili_sorular(hap_duz, section, adet=5, min_ortusme=3):
    """Aynı bölümde hap bilgiyle en az 3 *ayırt edici* kök paylaşan sorular.
    "kazazede", "sürücü" gibi bölümün sorularının %12'sinden fazlasında geçen
    kökler sayılmaz; yoksa her ilk yardım hap bilgisi her ilk yardım sorusuyla eşleşir."""
    df = soru_df(section)
    n = df.get("_n", 0)
    if not n:
        return []
    esik = max(2, int(n * 0.12))
    hk = {k for k in kokler(hap_duz) if df.get(k, 0) <= esik}
    adaylar = []
    for bolum, slug, baslik, sk in sorulari_yukle():
        if bolum != section:
            continue
        ortak = hk & sk
        if len(ortak) >= min_ortusme:
            agirlik = sum(1.0 / df.get(k, 1) for k in ortak)  # nadir kök daha değerli
            adaylar.append((-len(ortak), -agirlik, baslik, slug))
    adaylar.sort()
    return [(slug, baslik) for _, _, baslik, slug in adaylar[:adet]]


def baglam_paragrafi(kategori_ad, grup_ad, ders, satirlar):
    cumleler = [f"Bu bilgi, {esc(kategori_ad)} hap bilgilerinde <b>{esc(grup_ad)}</b> başlığı altında yer alır."]
    if ders and satirlar:
        cumleler.append(f"Konunun ayrıntısı <b>{esc(ders['lesson'])}</b> ders notundadır; aynı ders notundan: "
                        + " ".join(esc(s) for s in satirlar))
    elif ders:
        cumleler.append(f"Konunun ayrıntısı <b>{esc(ders['lesson'])}</b> ders notundadır.")
    cumleler.append("Sınavda bu tür bilgiler genellikle sayı, sıra ya da kural olarak doğrudan sorulur.")
    return " ".join(cumleler)


def generate_page(d, hap, onceki, sonraki, ders, satirlar):
    sira, grup_ad, bilgi_html, bilgi_duz, slug = hap
    kategori_ad = d["ad"]
    kat_slug = d["slug"]
    kat_url = f"/hap-bilgiler/{kat_slug}/"
    canonical = f"{DOMAIN}{kat_url}{slug}/"

    h1_text = truncate(bilgi_duz, 70)
    title_text = truncate(bilgi_duz, 52) + " | ehliyet.digital"
    desc_text = truncate(f"{kategori_ad} hap bilgi: {bilgi_duz}", 155)
    detay = detay_oku(slug)
    if detay and detay["baslik"]:
        h1_text = detay["baslik"]
        title_text = detay["baslik"] + " | ehliyet.digital"
    if detay and detay["aciklama"]:
        desc_text = detay["aciklama"]
    detay_html = ""
    if detay and detay["html"]:
        detay_html = "\n    <section class=\"detay\">\n" + detay["html"] + "\n    </section>\n"
    sorular = ilgili_sorular(bilgi_duz, kategori_ad)
    sorular_html = ""
    if sorular:
        sorular_html = ("\n    <h2 class=\"bolum\">Bu bilgi hangi sorularda çıkar?</h2>\n    <ul class=\"hap-sorular\">\n"
                        + "".join(f'      <li><a href="/soru/{s_}/">{esc(truncate(b_, 120))}</a></li>\n' for s_, b_ in sorular)
                        + "    </ul>\n")

    ders_url = ders["url"] if ders else SECTION_URL.get(kategori_ad, "/dersler/")
    ders_ad = ders["lesson"] if ders else f"{kategori_ad} ders notları"

    article_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1_text,
        "description": desc_text,
        "url": canonical,
        "inLanguage": "tr",
        "articleSection": kategori_ad,
        "datePublished": YAYIN_TARIHI,
        "author": {"@type": "Organization", "name": "ehliyet.digital", "url": f"{DOMAIN}/"},
        "publisher": {"@type": "Organization", "name": "ehliyet.digital", "url": f"{DOMAIN}/"},
        "about": {"@type": "Thing", "name": kategori_ad},
    }, ensure_ascii=False, indent=2)

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "Hap Bilgiler", "item": f"{DOMAIN}/hap-bilgiler/"},
            {"@type": "ListItem", "position": 3, "name": kategori_ad, "item": f"{DOMAIN}{kat_url}"},
            {"@type": "ListItem", "position": 4, "name": truncate(bilgi_duz, 60)},
        ]
    }, ensure_ascii=False, indent=2)

    nav_items = ""
    if onceki:
        nav_items += f'      <a class="hap-nav-link" href="{kat_url}{onceki[4]}/" rel="prev">&larr; {onceki[0]:02d}: {esc(truncate(onceki[3], 48))}</a>\n'
    if sonraki:
        nav_items += f'      <a class="hap-nav-link next" href="{kat_url}{sonraki[4]}/" rel="next">{sonraki[0]:02d}: {esc(truncate(sonraki[3], 48))} &rarr;</a>\n'

    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://www.gstatic.com" crossorigin>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<title>{esc(title_text)}</title>
<meta name="description" content="{esc(desc_text)}">
<link rel="canonical" href="{canonical}">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ehliyet Sınavı">
<meta property="og:title" content="{esc(h1_text)}">
<meta property="og:description" content="{esc(desc_text)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ehliyet.digital — Ehliyet sınavına hazırlık platformu">
<meta property="article:published_time" content="{YAYIN_TARIHI}">
<meta property="article:section" content="{esc(kategori_ad)}">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(h1_text)}">
<meta name="twitter:description" content="{esc(desc_text)}">
<meta name="twitter:image" content="{DOMAIN}/og-image.png">
<meta name="twitter:image:alt" content="ehliyet.digital — Ehliyet sınavına hazırlık platformu">

<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/css/fonts.css" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="/assets/css/fonts.css"></noscript>
<style>
  :root{{--fg:#08090a;--muted:#6a6f76;--line:#ececec;--bg:#fff}}
  *{{box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  body{{margin:0;font-family:'Inter','Inter-fallback',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    color:var(--fg);background:#fff;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;min-height:100vh;letter-spacing:-.011em;line-height:1.75}}
  a{{color:inherit}}

  header{{display:flex;align-items:center;gap:26px;height:64px;
    padding:0 max(28px, calc((100% - 1100px) / 2));border-bottom:1px solid var(--line);
    position:sticky;top:0;background:rgba(255,255,255,.8);backdrop-filter:saturate(180%) blur(10px);z-index:20}}
  .nav{{display:flex;gap:24px}}
  .nav a{{color:var(--muted);text-decoration:none;font-size:14px;font-weight:450;white-space:nowrap}}
  .nav a:hover{{color:var(--fg)}}

  main{{flex:1;max-width:760px;margin:0 auto;padding:52px 24px 96px;width:100%}}

  .breadcrumb{{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:0 0 24px}}
  .breadcrumb a{{color:var(--muted);text-decoration:none}}
  .breadcrumb a:hover{{color:var(--fg);text-decoration:underline;text-underline-offset:3px}}
  .breadcrumb .sep{{color:var(--muted);font-size:11px}}

  .eyebrow{{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}}
  h1{{font-size:clamp(22px,4vw,32px);font-weight:600;letter-spacing:-.025em;line-height:1.35;margin:0 0 28px}}

  .hap{{display:flex;gap:16px;align-items:flex-start;border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff;font-size:15px;line-height:1.62;margin:0 0 24px}}
  .hap b{{font-weight:600}}
  .hap-num{{font-family:'Geist Mono',monospace;font-size:12.5px;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:6px 9px;flex-shrink:0}}

  .baglam{{font-size:15px;line-height:1.7;color:#444;margin:0 0 32px}}
  h2.bolum,.detay h2{{font-size:19px;font-weight:600;letter-spacing:-.02em;margin:30px 0 10px;line-height:1.3}}
  .detay p{{font-size:15px;line-height:1.7;color:#333;margin:0 0 12px}}
  .detay ul,.detay ol{{font-size:15px;line-height:1.7;color:#333;padding-left:22px;margin:0 0 14px}}
  .detay li{{margin:0 0 6px}}
  .detay .detay-gorsel{{margin:16px 0 20px;border:1px solid var(--line);border-radius:14px;padding:16px;background:#fafafa;text-align:center}}
  .detay .detay-gorsel img{{max-width:100%;height:auto;max-height:320px;display:inline-block}}
  .detay figcaption{{margin-top:10px;font-size:13px;color:var(--muted);line-height:1.5}}
  .detay .kutu{{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:#fafafa;margin:0 0 14px;font-size:15px;line-height:1.6}}
  .hap-sorular{{list-style:none;padding:0;margin:0 0 32px;display:flex;flex-direction:column;gap:8px}}
  .hap-sorular a{{display:block;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:14px;line-height:1.5;color:var(--fg);text-decoration:none}}
  .hap-sorular a:hover{{border-color:#c8c8c8;background:#fafafa}}
  .baglam b{{font-weight:600;color:var(--fg)}}

  .ilgili{{margin-top:8px;padding-top:24px;border-top:1px solid var(--line);font-size:14px;line-height:1.6}}
  .ilgili p{{margin:0 0 8px}}
  .ilgili a{{font-weight:500;text-decoration:none}}
  .ilgili a:hover{{text-decoration:underline;text-underline-offset:3px}}

  .hap-nav{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:24px;padding-top:24px;border-top:1px solid var(--line)}}
  .hap-nav-link{{font-size:13px;color:var(--muted);text-decoration:none;max-width:48%}}
  .hap-nav-link.next{{margin-left:auto;text-align:right}}
  .hap-nav-link:hover{{color:var(--fg);text-decoration:underline;text-underline-offset:3px}}

  .kaynak{{margin-top:24px;font-size:13px;color:var(--muted);line-height:1.6}}

  .marka{{display:flex;align-items:center;flex-shrink:0;text-decoration:none}}
  .marka img{{width:26px;height:26px;object-fit:contain;display:block}}

  .site-footer{{border-top:1px solid var(--line);background:#fafafa;margin-top:auto;padding:0}}
  .foot-wrap{{max-width:1100px;margin:0 auto;padding:44px 28px 40px;display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:40px;align-items:start}}
  .foot-hakkinda{{display:flex;flex-direction:column;align-items:flex-start;gap:16px}}
  .foot-hakkinda p{{margin:0;font-size:14px;color:var(--muted);line-height:1.55;max-width:270px}}
  .foot-col{{display:flex;flex-direction:column;gap:10px}}
  .foot-label{{display:block;margin:0 0 4px;font-family:'Geist Mono',monospace;font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
  .foot-col a{{color:var(--fg);font-size:14px;text-decoration:none}}
  .foot-col a:hover{{text-decoration:underline;text-underline-offset:3px}}
  @media(max-width:860px){{.foot-wrap{{grid-template-columns:1fr 1fr;gap:30px}}.foot-hakkinda{{grid-column:1/-1}}}}
  .foot-feedback{{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line);background:#fff;border-radius:10px;padding:11px 18px;font-size:14px;font-weight:500;color:var(--fg);text-decoration:none;transition:.15s;white-space:nowrap}}
  .foot-feedback:hover{{border-color:#c8c8c8}}
  .foot-feedback svg{{color:var(--muted)}}
  .foot-marka{{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--fg);font-size:14.5px;font-weight:600;letter-spacing:-.02em;flex-shrink:0}}
  .foot-marka img{{width:22px;height:22px;object-fit:contain;display:block}}

  @media(max-width:640px){{
    header{{padding:0 16px;gap:12px;height:58px}}
    .nav{{gap:14px}}
    .nav a{{font-size:11px}}
    main{{padding:40px 20px 64px}}
    .marka img{{width:22px;height:22px}}
    .foot-wrap{{gap:26px}}
    .hap-nav-link{{max-width:100%}}
  }}
</style>

<link rel="alternate" type="application/rss+xml" title="ehliyet.digital RSS" href="/feed.xml">
<script type="application/ld+json">
{article_ld}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</head>
<body>

  <header>
    <a class="marka" href="/" aria-label="ehliyet.digital"><img src="/assets/img/marka/logo.png" alt="ehliyet.digital" width="26" height="26"></a>
    <nav class="nav" aria-label="Ana navigasyon">
      <a href="/">Ana Sayfa</a>
      <a href="/ehliyet-sinav-sorulari/">Soru Çöz</a>
      <a href="/dersler/">Ders Notları</a>
      <a href="/hap-bilgiler/">Hap Bilgiler</a>
    </nav>
  </header>

  <main>
    <nav class="breadcrumb" aria-label="Gezinme">
      <a href="/">Ana Sayfa</a> <span class="sep">›</span> <a href="/hap-bilgiler/">Hap Bilgiler</a> <span class="sep">›</span> <a href="{kat_url}">{esc(kategori_ad)}</a> <span class="sep">›</span> <span>{esc(truncate(bilgi_duz, 60))}</span>
    </nav>

    <p class="eyebrow">{esc(kategori_ad)} · {esc(grup_ad)}</p>
    <h1>{esc(h1_text)}</h1>

    <!-- BODY_START -->
    <div class="hap"><span class="hap-num">{sira:02d}</span><span>{bilgi_html}</span></div>
{detay_html}
    <h2 class="bolum">Ders notunda nasıl geçer?</h2>
    <p class="baglam">{baglam_paragrafi(kategori_ad, grup_ad, ders, satirlar)}</p>
{sorular_html}    <!-- BODY_END -->

    <div class="ilgili">
      <p>Bu bilgi <b>{esc(kategori_ad)}</b> konusuna aittir.
        <a href="{ders_url}">{esc(ders_ad)} &rarr;</a></p>
      <p><a href="{kat_url}">Tüm {esc(kategori_ad)} hap bilgileri &rarr;</a></p>
      <p><a href="/ehliyet-sinav-sorulari/{kat_slug}/">{esc(kategori_ad)} çıkmış sınav soruları &rarr;</a> · <a href="/deneme-sinavi/?konu={kat_slug}">Bu konudan deneme çöz &rarr;</a></p>
    </div>

    <nav class="hap-nav" aria-label="Önceki / sonraki hap bilgi">
{nav_items}    </nav>

    <div class="kaynak">
      <p>Kaynak: MEB MTSK e-sınavı</p>
    </div>
  </main>

  <footer class="site-footer">
    <div class="foot-wrap">
      <div class="foot-hakkinda">
        <a class="foot-marka" href="/">
          <img src="/assets/img/marka/logo.png" alt="ehliyet.digital" width="22" height="22" loading="lazy">
          ehliyet.digital
        </a>
        <p>Sınavdan önce ders notlarını incele, hap bilgileri al ve deneme sınavları ile kendini test et. Ehliyet sınavına kolaylıkla hazırlan.</p>
        <a class="foot-feedback" href="mailto:omerlhn@gmail.com?subject=Ehliyet%20Deneme%20—%20Geri%20Bildirim">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          Geri bildirim gönder
        </a>
      </div>
      <nav class="foot-col" aria-label="Hap Bilgiler">
        <span class="foot-label">Hap Bilgiler</span>
        <a href="/hap-bilgiler/ilk-yardim/">İlk Yardım</a>
        <a href="/hap-bilgiler/trafik-ve-cevre/">Trafik ve Çevre</a>
        <a href="/hap-bilgiler/arac-teknigi/">Araç Tekniği</a>
        <a href="/hap-bilgiler/trafik-adabi/">Trafik Adabı</a>
      </nav>
      <nav class="foot-col" aria-label="Ders Notları">
        <span class="foot-label">Ders Notları</span>
        <a href="/dersler/ilk-yardim/">İlk Yardım</a>
        <a href="/dersler/trafik-ve-cevre/">Trafik ve Çevre</a>
        <a href="/dersler/arac-teknigi/">Araç Tekniği</a>
        <a href="/dersler/trafik-adabi/">Trafik Adabı</a>
      </nav>
      <nav class="foot-col" aria-label="Faydalı Bilgiler">
        <span class="foot-label">Faydalı Bilgiler</span>
        <a href="/ehliyet-sinav-sorulari/">Soru Çöz</a>
        <a href="/ehliyet-nasil-alinir/">Ehliyet Nasıl Alınır?</a>
        <a href="/ehliyet-sinav-konulari/">Sınav Konuları</a>
        <a href="/direksiyon-sinavi/">Direksiyon Sınavı</a>
      </nav>
      <nav class="foot-col" aria-label="Sayfalar">
        <span class="foot-label">Sayfalar</span>
        <a href="/hakkinda/">Hakkında</a>
        <a href="/iletisim/">İletişim</a>
        <a href="/gizlilik/">Gizlilik Politikası</a>
        <a href="/kullanim-sartlari/">Kullanım Şartları</a>
      </nav>
    </div>
  </footer>

  <script src="/assets/js/mobile-nav.js" defer></script>
<!-- Google tag (gtag.js) -->
<script>
window.dataLayer=window.dataLayer||[];function g(){{dataLayer.push(arguments)}}window.gtag=g;g('js',new Date());g('config','G-34HL041XN0');var r=document.referrer,h=r?r.split('/')[2]:'';if(h&&/(chatgpt\\.com|openai\\.com|perplexity\\.ai|claude\\.ai|anthropic\\.com|gemini\\.google\\.com|copilot\\.microsoft\\.com|bing\\.com\\/chat|you\\.com|mistral\\.ai|deepseek\\.com)$/.test(h)){{g('event','ai_referral',{{ai_source:h}})}}
function loadGA(){{var s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-34HL041XN0';s.async=true;document.head.appendChild(s)}}
if(typeof requestIdleCallback==='function'){{requestIdleCallback(loadGA)}}else{{setTimeout(loadGA,2500)}}
</script>
</body>
</html>'''


# ---------------------------------------------------------------------------
# Kategori sayfalarına link ekleme
# ---------------------------------------------------------------------------

HAP_NUM_CSS = """  a.hap-num{text-decoration:none;transition:.12s}
  a.hap-num:hover{color:var(--fg);border-color:#c8c8c8;background:#fafafa}
"""


def kategori_sayfasini_linkle(d, haplar):
    path = os.path.join(HAP_DIR, d["slug"], "index.html")
    if not os.path.exists(path):
        print(f"  Uyari: {path} yok, link eklenemedi.")
        return
    with open(path, encoding="utf-8") as f:
        t = f.read()
    slug_by_num = {sira: slug for sira, _g, _h, _d, slug in haplar}

    def yeni(m):
        num = int(m.group(1))
        slug = slug_by_num.get(num)
        if not slug:
            return m.group(0)
        return (f'<a class="hap-num" href="/hap-bilgiler/{d["slug"]}/{slug}/" '
                f'aria-label="Hap bilgi {num:02d} sayfası">{num:02d}</a>')

    # Hem ilk üretimdeki <span> hem de daha önce eklenmiş <a> biçimini yakala (idempotent)
    t, n1 = re.subn(r'<span class="hap-num">(\d+)</span>', yeni, t)
    t, n2 = re.subn(r'<a class="hap-num" href="[^"]*"(?: aria-label="[^"]*")?>(\d+)</a>', yeni, t)

    if "a.hap-num{" not in t:
        t = re.sub(r"(  \.hap-num\{[^\n]*\}\n)", lambda m: m.group(1) + HAP_NUM_CSS, t, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print(f"  kategori linklendi: hap-bilgiler/{d['slug']}/index.html ({n1 + n2} link)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

HAP_BASLA = "<!-- HAP_LINKLERI_BASLA -->"
HAP_BITIR = "<!-- HAP_LINKLERI_BITIR -->"


def ders_sayfalarini_linkle(ders_haplari):
    """Ders sayfalarının 'İlgili Kaynaklar' bloğuna o derse eşlenen hap
    bilgilerin listesini ekler. İşaretçiler arası silinip yeniden yazılır;
    eşleme kalmayan derste blok kaldırılır."""
    yazilan = 0
    for ders_path in sorted(pathlib.Path(ROOT, "dersler").glob("*/*/index.html")):
        url = "/" + ders_path.parent.relative_to(ROOT).as_posix() + "/"
        t = ders_path.read_text(encoding="utf-8")
        t = re.sub(rf"\n?\s*{re.escape(HAP_BASLA)}.*?{re.escape(HAP_BITIR)}", "", t, flags=re.S)
        h2css = ".ilgili-konular h2{font-size:17px;margin:0 0 12px}"
        h3css = ".ilgili-konular h3{font-size:15px;margin:20px 0 10px}"
        if h2css in t and h3css not in t:
            t = t.replace(h2css, h2css + "\n" + h3css)
        haplar = ders_haplari.get(url)
        if haplar:
            m = re.search(r'<div class="ilgili-konular">.*?</ul>', t, re.S)
            if m:
                blok = f"\n      {HAP_BASLA}\n      <h3>Bu konunun hap bilgileri</h3>\n      <ul>\n"
                for hap_url, metin in haplar:
                    blok += f'        <li><a href="{hap_url}">{esc(truncate(metin, 110))}</a></li>\n'
                blok += f"      </ul>\n      {HAP_BITIR}"
                t = t[:m.end()] + blok + t[m.end():]
                yazilan += 1
        ders_path.write_text(t, encoding="utf-8")
    return yazilan


def main():
    dersler = dersleri_yukle()

    # Düz metin doğrulaması: quick-facts.json ile DERSLER aynı sırada olmalı
    with open(os.path.join(DATA_DIR, "quick-facts.json"), encoding="utf-8") as f:
        quick = json.load(f)
    tum = [(d, h) for d in DERSLER for h in hap_listesi(d)]
    if len(quick) != len(tum):
        print(f"  Uyari: quick-facts.json {len(quick)} kayit, DERSLER {len(tum)} hap; DERSLER esas alindi.")
    else:
        for (d, h), q in zip(tum, quick):
            if q["fact"] != h[3] or q["section"] != d["ad"]:
                print(f"  Uyari: sira {h[0]} ({d['slug']}) quick-facts.json ile uyusmuyor.")

    generated = 0
    hub = 0
    ders_haplari = {}
    for d in DERSLER:
        haplar = hap_listesi(d)
        kat_dir = os.path.join(HAP_DIR, d["slug"])
        os.makedirs(kat_dir, exist_ok=True)

        # Artık slug klasörlerini temizle (idempotent)
        gecerli = {h[4] for h in haplar}
        for ad in os.listdir(kat_dir):
            p = os.path.join(kat_dir, ad)
            if os.path.isdir(p) and ad not in gecerli:
                shutil.rmtree(p)

        for i, hap in enumerate(haplar):
            onceki = haplar[i - 1] if i > 0 else None
            sonraki = haplar[i + 1] if i + 1 < len(haplar) else None
            ders = en_iyi_ders(hap[3], d["ad"], dersler)
            satirlar = ilgili_satirlar(hap[3], ders) if ders else []
            if not ders:
                hub += 1
            else:
                ders_haplari.setdefault(ders["url"], []).append((f"/hap-bilgiler/{d['slug']}/{hap[4]}/", hap[3]))
            page_dir = os.path.join(kat_dir, hap[4])
            os.makedirs(page_dir, exist_ok=True)
            with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(generate_page(d, hap, onceki, sonraki, ders, satirlar))
            generated += 1

        kategori_sayfasini_linkle(d, haplar)

    dersli = ders_sayfalarini_linkle(ders_haplari)
    print(f"\n  Uretilen sayfa: {generated}")
    print(f"  Hap listesi eklenen ders sayfasi: {dersli}")
    print(f"  Ders eslenemeyip hub'a baglanan: {hub}")


if __name__ == "__main__":
    main()
