#!/usr/bin/env python3
"""Konu bazlı soru dizini sayfalarını üretir: /ehliyet-sinav-sorulari/{konu}/index.html

Her sayfa o konunun çıkmış sorularını (/soru/ sayfalarına bağlantı), sınavda
en çok çıkan hap bilgileri ve ders notlarını tek yerde toplar; konu denemesine
(/deneme-sinavi/?konu=...) yönlendirir. Hedef sorgular "ehliyet motor soruları",
"ehliyet ilk yardım soruları" gibi konu + soru kalıplarıdır.

Kullanım (depo kökünden):  python3 tools/konu-sayfa-uret.py
Soru, hap ya da ders eklendiğinde tekrar çalıştırılır; sonra schema-uret ve
sitemap-uret çalıştırılmalıdır.

Veri kaynakları sayfaların kendisidir (soru sayfası h1'i, hap kategori dizini,
ders kategori dizini); ikinci bir liste tutulmaz.
"""
import html as H
import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ehliyet.digital"

KONULAR = [
    {
        "slug": "ilk-yardim", "ad": "İlk Yardım", "sinavda": 12,
        "kisa": "ilk yardım",
        "giris": ("Ehliyet sınavında İlk Yardım bölümünden <b>12 soru</b> gelir. Sorular temel yaşam desteği, "
                  "kanamalar, kırık-çıkık, şok ve koma pozisyonları, taşıma teknikleri ve hava yolu açma gibi "
                  "konulardan çıkar. Çoğu soru sayı, sıra ya da pozisyon adı sorar; ezber gerektiren ama "
                  "kısa sürede toplanan bir bölümdür."),
    },
    {
        "slug": "trafik-ve-cevre", "ad": "Trafik ve Çevre", "sinavda": 23,
        "kisa": "trafik",
        "giris": ("Ehliyet sınavının en ağır bölümü: 50 sorunun <b>23'ü</b> Trafik ve Çevre'den gelir. Hız sınırları, "
                  "geçiş hakkı ve geçiş üstünlüğü, duraklama-park kuralları, trafik işaretleri, kavşaklar, "
                  "ceza puanları ve belge süreleri en çok sorulan başlıklardır. Bu bölümde iyi olmak sınavı "
                  "geçmenin en kısa yoludur."),
    },
    {
        "slug": "arac-teknigi", "ad": "Araç Tekniği", "sinavda": 9,
        "kisa": "motor",
        "giris": ("Ehliyet sınavında Araç Tekniği (motor) bölümünden <b>9 soru</b> gelir. Sorular gösterge "
                  "paneli ikaz lambaları, fren ve el freni, yağlama ve soğutma sistemi, akü ve şarj, "
                  "lastik basıncı, yakıt tasarrufu ve araç muayenesi gibi konulardan çıkar. Aynı bilgiler "
                  "her sınavda farklı cümlelerle sorulur."),
    },
    {
        "slug": "trafik-adabi", "ad": "Trafik Adabı", "sinavda": 6,
        "kisa": "trafik adabı",
        "giris": ("Ehliyet sınavında Trafik Adabı bölümünden <b>6 soru</b> gelir. Sorular diğerkâmlık, feragat, "
                  "empati, öfke ve stres yönetimi, iletişim ve toplum adabına aykırı davranışlar gibi "
                  "kavramları tanımlarıyla sorar. Doğru cevap çoğu zaman en ölçülü ve saygılı seçenektir."),
    },
]
SIRA = {k["ad"]: i for i, k in enumerate(KONULAR)}


def modul_yukle(ad, yol):
    spec = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def soru_sinav_haritasi():
    """slug -> sınav numarası; soru-sayfa-uret.py ile aynı slug mantığı."""
    su = modul_yukle("soru_uret", ROOT / "tools" / "soru-sayfa-uret.py")
    kullanilan, harita = set(), {}
    for i in range(1, 5):
        js = su.read_js_file(str(ROOT / "assets" / "js" / f"questions-{i}.js"))
        for q in su.extract_questions(js):
            if su.should_skip(q) or not q["stem"].strip() or len(q["options"]) < 2:
                continue
            slug = su.slugify(q["stem"])
            if not slug:
                continue
            temel, sayac = slug, 2
            while slug in kullanilan:
                slug = f"{temel}-{sayac}"
                sayac += 1
            kullanilan.add(slug)
            harita[slug] = i
    return harita


def sorular():
    """Konu adı -> [(slug, başlık, sınav no)]; soru sayfalarından okunur."""
    harita = soru_sinav_haritasi()
    sonuc = {}
    for d in sorted((ROOT / "soru").iterdir()):
        f = d / "index.html"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)
        h1 = re.sub(r"<br\s*/?>", " ", h1)  # "I. LPG<br>II. Benzin" -> "I. LPG II. Benzin"
        baslik = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", h1))).strip()
        konu = re.search(r"Bu soru <b>([^<]+)</b> konusuna aittir", t).group(1)
        sonuc.setdefault(konu, []).append((d.name, baslik, harita.get(d.name, 0)))
    return sonuc


def hap_bilgiler(slug, adet=8):
    """Kategori dizinindeki ilk N hap bilgi: (url, html metin)."""
    t = (ROOT / "hap-bilgiler" / slug / "index.html").read_text(encoding="utf-8")
    ogeler = re.findall(
        r'<a class="hap-num" href="(/hap-bilgiler/' + re.escape(slug) + r'/[^"]+)"[^>]*>\d+</a><span>(.*?)</span>',
        t, re.S)
    return ogeler[:adet]


def dersler(slug):
    """Kategori dizinindeki ders bağlantıları: (url, ad)."""
    t = (ROOT / "dersler" / slug / "index.html").read_text(encoding="utf-8")
    bulunan, sonuc = set(), []
    for url, ic in re.findall(r'<a[^>]+href="(/dersler/' + re.escape(slug) + r'/[^"/]+/)"[^>]*>(.*?)</a>', t, re.S):
        ad = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", ic))).strip()
        m = re.search(r'<span class="lesson-title">(.*?)</span>', ic, re.S) or re.search(r"<h3[^>]*>(.*?)</h3>", ic, re.S)
        if m:
            ad = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
        if url in bulunan or not ad:
            continue
        bulunan.add(url)
        sonuc.append((url, ad))
    return sonuc


def kisalt(b, n=120):
    return b if len(b) <= n else b[:n].rsplit(" ", 1)[0] + "…"


def kabuk():
    """Nav, footer, GA ve stil pillar sayfasından alınır; tek kaynak."""
    p = (ROOT / "ehliyet-sinav-sorulari" / "index.html").read_text(encoding="utf-8")
    stil = p[p.index("<style>"):p.index("</style>") + len("</style>")]
    header = p[p.index("<body>\n") + len("<body>\n"):p.index("  <main>")]
    footer = p[p.index('  <footer class="site-footer">'):p.index("  </footer>") + len("  </footer>")]
    ga_bas = "<!-- Google tag (gtag.js) — sayfa yüklendikten sonra yüklenir -->"
    ga = p[p.index(ga_bas):p.index("</body>")]
    return stil, header, footer, ga


EK_CSS = """
  /* Konu sayfası */
  .ozet{display:flex;gap:28px;flex-wrap:wrap;margin-top:28px}
  .ozet div{display:flex;flex-direction:column;gap:2px}
  .ozet b{font-size:26px;font-weight:600;letter-spacing:-.03em;line-height:1}
  .ozet span{font-size:13px;color:var(--muted)}
  .hap-liste{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
  @media(max-width:760px){.hap-liste{grid-template-columns:1fr}}
  .hap-liste li{border:1px solid var(--line);border-radius:12px;padding:12px 14px 12px 44px;position:relative;font-size:14px;line-height:1.55;color:#333}
  .hap-liste li span.no{position:absolute;left:14px;top:12px;font-family:'Geist Mono',monospace;font-size:12px;color:var(--muted)}
  .hap-liste li a{color:inherit;text-decoration:none}
  .hap-liste li a:hover{text-decoration:underline;text-underline-offset:3px}
  .konu-sorular{list-style:none;margin:0;padding:0;columns:2;column-gap:32px}
  @media(max-width:760px){.konu-sorular{columns:1}}
  .konu-sorular li{font-size:14px;line-height:1.5;margin:0 0 10px;break-inside:avoid;padding-left:22px;position:relative}
  .konu-sorular li::before{content:attr(data-no);position:absolute;left:0;top:1px;font-family:'Geist Mono',monospace;font-size:12px;color:var(--muted)}
  .konu-sorular a{color:var(--fg);text-decoration:none}
  .konu-sorular a:hover{text-decoration:underline;text-underline-offset:3px}
  .konu-sorular .sinav{font-family:'Geist Mono',monospace;font-size:11px;color:var(--muted);margin-left:6px;white-space:nowrap}
  .ders-liste{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
  .ders-liste a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:13.5px;color:var(--fg);text-decoration:none}
  .ders-liste a:hover{border-color:#c8c8c8;background:#fafafa}
  .konu-nav{display:flex;flex-wrap:wrap;gap:8px}
  .konu-nav a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:13.5px;color:var(--fg);text-decoration:none}
  .konu-nav a[aria-current]{background:#08090a;color:#fff;border-color:#08090a}
"""


def sayfa(konu, liste, stil, header, footer, ga):
    slug, ad = konu["slug"], konu["ad"]
    n = len(liste)
    url = f"{BASE}/ehliyet-sinav-sorulari/{slug}/"
    title = f"{ad} Ehliyet Sınav Soruları: {n} Çıkmış Soru ve Cevabı"
    desc = (f"Ehliyet sınavında {ad} bölümünden çıkmış {n} soru ve cevabı. Sınavda bu konudan {konu['sinavda']} soru gelir. "
            f"Soruları incele ya da sadece {konu['kisa']} denemesini çöz.")
    assert len(desc) <= 165, (slug, len(desc))

    haplar = hap_bilgiler(slug)
    hap_html = "\n".join(
        f'          <li><span class="no">{i+1:02d}</span><a href="{u}">{m}</a></li>'
        for i, (u, m) in enumerate(haplar))
    soru_html = "\n".join(
        f'          <li data-no="{i+1}"><a href="/soru/{s}/">{H.escape(kisalt(b))}</a>'
        + (f'<span class="sinav">Sınav {e}</span>' if e else "") + "</li>"
        for i, (s, b, e) in enumerate(liste))
    ders_html = "\n".join(f'          <li><a href="{u}">{H.escape(a)}</a></li>' for u, a in dersler(slug))
    nav_html = "\n".join(
        f'          <a href="/ehliyet-sinav-sorulari/{k["slug"]}/"' + (' aria-current="page"' if k["slug"] == slug else "") + f'>{k["ad"]}</a>'
        for k in KONULAR)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://www.gstatic.com" crossorigin>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="ehliyet.digital">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ehliyet.digital — {ad} sınav soruları">
<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/og-image.png">
<meta name="twitter:image:alt" content="ehliyet.digital — {ad} sınav soruları">
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/css/fonts.css" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="/assets/css/fonts.css"></noscript>
<link rel="alternate" type="application/rss+xml" title="ehliyet.digital RSS" href="/feed.xml">
{stil.replace("</style>", EK_CSS + "</style>")}
</head>
<body>
{header}  <main>
    <div class="hero">
      <nav class="breadcrumb" aria-label="Gezinme">
        <a href="/">Ana Sayfa</a> <span class="sep">›</span> <a href="/ehliyet-sinav-sorulari/">Ehliyet Sınav Soruları</a> <span class="sep">›</span> <span>{ad}</span>
      </nav>
      <h1>{ad} Ehliyet Sınav Soruları</h1>
      <p>{konu["giris"]}</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="/deneme-sinavi/?konu={slug}">{ad} Denemesine Başla</a>
        <a class="btn btn-outline btn-lg" href="#sorular">{n} soruyu incele</a>
      </div>
      <div class="ozet" aria-label="Özet">
        <div><b>{konu["sinavda"]}</b><span>sınavda soru</span></div>
        <div><b>{n}</b><span>çıkmış soru</span></div>
        <div><b>{len(haplar)}</b><span>hap bilgi</span></div>
      </div>
    </div>

    <div class="icerik">
      <section class="soru-grup">
        <h2>Sınavda en çok çıkan {ad.lower() if slug != "ilk-yardim" else "ilk yardım"} bilgileri</h2>
        <p class="grup-desc">Aşağıdaki bilgiler bu bölümdeki soruların çoğunu doğrudan çözdürür. Tamamı için <a href="/hap-bilgiler/{slug}/">{ad} hap bilgileri</a> sayfasına bak.</p>
        <ul class="hap-liste">
{hap_html}
        </ul>
      </section>

      <section class="soru-grup" id="sorular">
        <h2>{ad} çıkmış sorular ({n})</h2>
        <p class="grup-desc">MEB e-sınavında çıkmış {ad} soruları. Her bağlantıda soru, şıklar ve doğru cevap var; yanındaki etiket sorunun hangi denemede olduğunu gösterir.</p>
        <ol class="konu-sorular">
{soru_html}
        </ol>
      </section>

      <section class="soru-grup">
        <h2>{ad} ders notları</h2>
        <p class="grup-desc">Yanlış yaptığın soruların konusunu buradan tekrar et.</p>
        <ul class="ders-liste">
{ders_html}
        </ul>
      </section>

      <section class="soru-grup">
        <h2>Diğer konular</h2>
        <nav class="konu-nav" aria-label="Konular">
{nav_html}
        </nav>
      </section>
    </div>

    <section class="cta">
      <div class="cta-inner">
        <h2>{ad} sorularında kendini dene</h2>
        <p>Dört sınavın {ad} soruları tek denemede, gerçek sınav formatında. Giriş gerekmez, süre soru sayısına göre ayarlanır.</p>
        <a class="btn btn-primary btn-lg" href="/deneme-sinavi/?konu={slug}">{ad} Denemesine Başla</a>
        <p style="margin-top:14px"><a href="/deneme-sinavi/" style="font-size:14px;color:var(--muted)">ya da 50 soruluk tam denemeyi çöz →</a></p>
      </div>
    </section>
  </main>
{footer}
  <script src="/assets/js/feedback.js" defer></script>
  <script type="module" src="/assets/js/auth-ui.js"></script>
  <script src="/assets/js/mobile-nav.js" defer></script>
{ga}</body>
</html>
"""


PILLAR_BAS = "<!-- TUM_SORULAR_BASLA: tools/konu-sayfa-uret.py üretir, elle düzenlenmez -->"
PILLAR_SON = "<!-- TUM_SORULAR_BITIR -->"


def pillar_listesi(tum):
    """/ehliyet-sinav-sorulari/ sayfasındaki 186 soruluk dizin; işaretçiler arası yenilenir."""
    toplam = sum(len(v) for v in tum.values())
    blok = [PILLAR_BAS,
            '    <section class="soru-grup" id="tum-sorular" style="max-width:1100px;margin:0 auto;padding:32px 28px">',
            '      <h2>Tüm Ehliyet Sınav Soruları</h2>',
            f'      <p class="grup-desc">Dört denemedeki {toplam} sorunun tamamı, konuya göre. Her bağlantıda sorunun cevabı ve açıklaması var.</p>']
    for k in KONULAR:
        liste = tum.get(k["ad"], [])
        blok.append('      <details class="soru-liste" open>')
        blok.append(f'        <summary>{k["ad"]} <span>({len(liste)} soru)</span> <a href="/ehliyet-sinav-sorulari/{k["slug"]}/" style="margin-left:auto;font-size:13px;font-weight:500">Konu sayfası →</a></summary>')
        blok.append('        <ol>')
        for slug, b, _e in liste:
            blok.append(f'          <li><a href="/soru/{slug}/">{H.escape(kisalt(b, 110))}</a></li>')
        blok.append('        </ol>')
        blok.append('      </details>')
    blok += ['    </section>', PILLAR_SON]
    return "\n".join(blok) + "\n"


def pillar_guncelle(tum):
    p = ROOT / "ehliyet-sinav-sorulari" / "index.html"
    s = p.read_text(encoding="utf-8")
    if PILLAR_BAS in s:
        a, b = s.index(PILLAR_BAS), s.index(PILLAR_SON) + len(PILLAR_SON) + 1
    else:  # ilk çalıştırma: elle yazılmış bölümü işaretçilerle sar
        a = s.index('    <section class="soru-grup" id="tum-sorular"')
        b = s.index("    </section>\n", a) + len("    </section>\n")
    s = s[:a] + pillar_listesi(tum) + s[b:]
    p.write_text(s, encoding="utf-8")
    print("  ehliyet-sinav-sorulari/index.html: tüm sorular dizini yenilendi")


def main():
    stil, header, footer, ga = kabuk()
    tum = sorular()
    pillar_guncelle(tum)
    for konu in KONULAR:
        liste = tum.get(konu["ad"], [])
        if not liste:
            raise SystemExit(f"{konu['ad']} için soru bulunamadı")
        hedef = ROOT / "ehliyet-sinav-sorulari" / konu["slug"] / "index.html"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        hedef.write_text(sayfa(konu, liste, stil, header, footer, ga), encoding="utf-8")
        print(f"  {hedef.relative_to(ROOT)}: {len(liste)} soru, {len(hap_bilgiler(konu['slug']))} hap, {len(dersler(konu['slug']))} ders")


if __name__ == "__main__":
    main()
