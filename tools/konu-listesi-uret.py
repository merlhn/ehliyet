#!/usr/bin/env python3
"""
Ders listelerini tek kaynaktan (assets/js/lessons-nav.js) üretir ve şu sayfalarda
işaretli blokları yeniden yazar:

- ehliyet-sinav-konulari/index.html  <!-- konu-listesi:<ders> --> … <!-- /konu-listesi:<ders> -->
    Her dersin altındaki konu listesi: konu adı (ders linki) + "Kısaca" kutusunun ilk cümlesi.
- dersler/<ders>/index.html          <!-- ders-ozetleri --> … <!-- /ders-ozetleri -->
    Dersin tüm konularının tek sayfada özeti ("ders notları" aramasını karşılar).
- dersler/index.html                 <!-- tum-dersler --> … <!-- /tum-dersler -->
    4 dersin tüm konuları, kısa açıklamalarıyla; ayrıca kart sayaçları ("N Konu").

Özetler her ders sayfasının .kisa-cevap kutusundan okunur; ayrı bir metin tutulmaz.
Yeni ders eklendiğinde (ders-notu ajanı lessons-nav.js'e yazar) bu script yeniden
çalıştırılır. Ders sayfası olmayan ek kaynaklar (ör. /trafik-isaretleri/) EKSTRA'dan
gelir ve yalnızca klasörü varsa listelenir.
"""

import html as H
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# lessons-nav.js'teki ders adı -> (klasör, sınav sorusu, görünen ad)
DERSLER = {
    "trafik-ve-cevre": (23, "Trafik ve Çevre Bilgisi"),
    "ilk-yardim": (12, "İlk Yardım"),
    "arac-teknigi": (9, "Araç Tekniği (Motor)"),
    "trafik-adabi": (6, "Trafik Adabı"),
}

EKSTRA = {
    "trafik-ve-cevre": [
        ("Trafik İşaretleri ve Anlamları", "/trafik-isaretleri/",
         "Tehlike uyarı, trafik tanzim ve bilgi işaretleri ile yer işaretlemeleri, görselleriyle."),
    ],
}


def dersleri_oku():
    """lessons-nav.js -> {klasör: [(n, başlık, url)]}"""
    js = (ROOT / "assets" / "js" / "lessons-nav.js").read_text(encoding="utf-8")
    sonuc = {}
    for n, baslik, url in re.findall(r'\{n:(\d+),title:"([^"]+)",url:"([^"]+)"\}', js):
        klasor = url.strip("/").split("/")[1]
        sonuc.setdefault(klasor, []).append((int(n), baslik, url))
    for k in sonuc:
        sonuc[k].sort()
    return sonuc


def duz(metin):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", metin))).strip()


def kisaca(url):
    """Ders sayfasının Kısaca kutusundaki ilk paragraf (düz metin)."""
    yol = ROOT / url.strip("/") / "index.html"
    if not yol.exists():
        return ""
    s = yol.read_text(encoding="utf-8")
    m = re.search(r'<div class="kisa-cevap">.*?<p>(.*?)</p>', s, re.S)
    if m:
        return duz(m.group(1))
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    return H.unescape(m.group(1)) if m else ""


def cumleler(metin, adet, sinir=None):
    """İlk `adet` cümle; `sinir` verilirse o uzunluğu aşmadan."""
    parcalar = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9])", metin)
    secilen = []
    for p in parcalar[:adet]:
        if sinir and secilen and len(" ".join(secilen + [p])) > sinir:
            break
        secilen.append(p)
    sonuc = " ".join(secilen)
    if sinir and len(sonuc) > sinir:
        sonuc = sonuc[: sinir - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return sonuc


def blok_yaz(yol, ad, icerik, girinti):
    s = yol.read_text(encoding="utf-8")
    bas, son = f"<!-- {ad} -->", f"<!-- /{ad} -->"
    desen = re.compile(re.escape(bas) + r".*?" + re.escape(son), re.S)
    if not desen.search(s):
        raise SystemExit(f"{yol.relative_to(ROOT)}: {bas} işareti yok")
    yeni = f"{bas}\n{icerik}\n{girinti}{son}"
    s2 = desen.sub(lambda _: yeni, s, count=1)
    if s2 != s:
        yol.write_text(s2, encoding="utf-8")
        return True
    return False


def ekstralar(klasor):
    return [e for e in EKSTRA.get(klasor, []) if (ROOT / e[1].strip("/") / "index.html").exists()]


def konular_sayfasi(dersler):
    yol = ROOT / "ehliyet-sinav-konulari" / "index.html"
    for klasor in DERSLER:
        g = " " * 6
        satirlar = [f"{g}<ul class=\"konu-listesi\">"]
        for _n, baslik, url in dersler.get(klasor, []):
            ozet = cumleler(kisaca(url), 1, 150)
            satirlar.append(f'{g}  <li><a class="inline" href="{url}"><b>{H.escape(baslik)}</b></a> — {H.escape(ozet)}</li>')
        for baslik, url, ozet in ekstralar(klasor):
            satirlar.append(f'{g}  <li><a class="inline" href="{url}"><b>{H.escape(baslik)}</b></a> — {H.escape(ozet)}</li>')
        satirlar.append(f"{g}</ul>")
        blok_yaz(yol, f"konu-listesi:{klasor}", "\n".join(satirlar), g)


def ders_hublari(dersler):
    for klasor, (_soru, ad) in DERSLER.items():
        yol = ROOT / "dersler" / klasor / "index.html"
        konular = dersler.get(klasor, [])
        g = " " * 4
        satirlar = [
            f'{g}<section class="ders-ozetleri" aria-labelledby="ozet-baslik">',
            f'{g}  <h2 id="ozet-baslik">{H.escape(ad)} ders notları: {len(konular)} konunun özeti</h2>',
            f'{g}  <p class="ozet-giris">Sınavdan önce son tekrar için her konunun en çok sorulan bilgisi tek sayfada. '
            f'Ayrıntı için konu başlığına tıkla. <button type="button" class="yazdir" onclick="window.print()">Bu sayfayı yazdır</button></p>',
        ]
        for n, baslik, url in konular:
            ozet = cumleler(kisaca(url), 3, 420)
            satirlar += [
                f'{g}  <div class="ozet">',
                f'{g}    <h3><span class="ozet-no">{n:02d}</span> <a href="{url}">{H.escape(baslik)}</a></h3>',
                f"{g}    <p>{H.escape(ozet)}</p>",
                f"{g}  </div>",
            ]
        for baslik, url, ozet in ekstralar(klasor):
            satirlar += [
                f'{g}  <div class="ozet">',
                f'{g}    <h3><a href="{url}">{H.escape(baslik)}</a></h3>',
                f"{g}    <p>{H.escape(ozet)}</p>",
                f"{g}  </div>",
            ]
        satirlar.append(f"{g}</section>")
        blok_yaz(yol, "ders-ozetleri", "\n".join(satirlar), g)


def tum_dersler(dersler):
    yol = ROOT / "dersler" / "index.html"
    toplam = sum(len(dersler.get(k, [])) for k in DERSLER)
    g = " " * 8
    satirlar = [f'{g}<h2 class="sec-title" style="margin-top:48px">Tüm Ders Notları ({toplam} Konu)</h2>']
    # Sayfadaki sıra: İlk Yardım, Trafik ve Çevre, Araç Tekniği, Trafik Adabı
    for klasor in ("ilk-yardim", "trafik-ve-cevre", "arac-teknigi", "trafik-adabi"):
        konular = dersler.get(klasor, [])
        satirlar.append("")
        satirlar.append(f"{g}<h3>{H.escape(DERSLER[klasor][1])} ({len(konular)} Konu)</h3>")
        satirlar.append(f'{g}<ol class="lesson-flat">')
        for _n, baslik, url in konular:
            ozet = cumleler(kisaca(url), 1, 120)
            satirlar.append(f'{g}  <li><a href="{url}">{H.escape(baslik)}</a><span class="lf-ozet">{H.escape(ozet)}</span></li>')
        satirlar.append(f"{g}</ol>")
        for baslik, url, ozet in ekstralar(klasor):
            satirlar.append(f'{g}<p class="lf-ekstra">Ayrıca: <a href="{url}">{H.escape(baslik)}</a></p>')
    blok_yaz(yol, "tum-dersler", "\n".join(satirlar), g)

    # Kart sayaçları: <a class="cat-block" href="/dersler/<klasör>/"> … <span class="cat-count">N Konu</span>
    s = yol.read_text(encoding="utf-8")
    for klasor in DERSLER:
        s = re.sub(
            r'(<a class="cat-block" href="/dersler/' + klasor + r'/">.*?<span class="cat-count">)\d+( Konu</span>)',
            lambda m, n=len(dersler.get(klasor, [])): f"{m.group(1)}{n}{m.group(2)}", s, count=1, flags=re.S)
    yol.write_text(s, encoding="utf-8")
    return toplam


if __name__ == "__main__":
    d = dersleri_oku()
    konular_sayfasi(d)
    ders_hublari(d)
    toplam = tum_dersler(d)
    for k in DERSLER:
        print(f"  {k}: {len(d.get(k, []))} konu, ekstra {len(ekstralar(k))}")
    print(f"  toplam: {toplam} konu")
