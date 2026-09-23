#!/usr/bin/env python3
"""llms-full.txt dosyasını site içeriğinden otomatik üretir.

Kullanım (depo kökünden):  python3 tools/llms-uret.py

Her ders sayfasının başlığını, açıklamasını ve ana içerik özetini
(h2 başlıkları) çıkarır. Yeni ders eklendiğinde tekrar çalıştırılır.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ehliyet.digital"

KATEGORI_SIRASI = ["ilk-yardim", "trafik-ve-cevre", "arac-teknigi", "trafik-adabi"]
KATEGORI_ADI = {
    "ilk-yardim": "İlk Yardım",
    "trafik-ve-cevre": "Trafik ve Çevre",
    "arac-teknigi": "Araç Tekniği (Motor)",
    "trafik-adabi": "Trafik Adabı",
}


def metin(kalip, t, grup=1):
    m = re.search(kalip, t, re.S)
    return re.sub(r"<[^>]+>", "", m.group(grup)).strip() if m else None


def h2ler(t):
    """Sayfadaki tüm h2 başlıklarını döndürür."""
    return [re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S)]


def paragraf_ozeti(t):
    """İlk anlamlı paragrafı (lead) döndürür."""
    m = re.search(r'<p class="lead">(.*?)</p>', t, re.S)
    if not m:
        m = re.search(r"<main[^>]*>.*?<p>(.*?)</p>", t, re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return None


# Ders sayfalarını topla
kategoriler = {}
for p in sorted(ROOT.rglob("index.html")):
    parcalar = p.relative_to(ROOT).parts
    if len(parcalar) != 4 or parcalar[0] != "dersler":
        continue
    kategori = parcalar[1]
    if kategori not in KATEGORI_ADI:
        continue
    t = p.read_text(encoding="utf-8")
    baslik = metin(r"<h1[^>]*>(.*?)</h1>", t) or ""
    aciklama = metin(r'<meta name="description" content="([^"]+)">', t) or ""
    h2_listesi = h2ler(t)
    lead = paragraf_ozeti(t)
    dizin = p.parent.relative_to(ROOT).as_posix()
    url = f"{BASE}/{dizin}/"

    kategoriler.setdefault(kategori, []).append({
        "baslik": baslik,
        "aciklama": aciklama,
        "url": url,
        "h2": h2_listesi,
        "lead": lead,
    })

# Hub sayfalarının açıklamalarını topla
hub_aciklamalari = {}
for kat in KATEGORI_SIRASI:
    hub = ROOT / "dersler" / kat / "index.html"
    if hub.exists():
        t = hub.read_text(encoding="utf-8")
        hub_aciklamalari[kat] = metin(r'<meta name="description" content="([^"]+)">', t) or ""

# llms-full.txt üret
satirlar = []
satirlar.append("# ehliyet.digital — Tam İçerik Dizini")
satirlar.append("")
satirlar.append("> Türkiye ehliyet sınavına ücretsiz hazırlık platformu.")
satirlar.append("> MEB MTSK müfredatına uygun 43 ders notu, 80 hap bilgi ve deneme sınavları.")
satirlar.append("> Dil: Türkçe | Konu: B sınıfı ehliyet teorik sınavı")
satirlar.append("")
satirlar.append("Bu dosya AI/LLM sistemlerinin site içeriğini hızlıca kavraması için üretilmiştir.")
satirlar.append("Kısa versiyon: https://ehliyet.digital/llms.txt")
satirlar.append("")

for kat in KATEGORI_SIRASI:
    dersler = kategoriler.get(kat, [])
    if not dersler:
        continue
    satirlar.append(f"---")
    satirlar.append(f"")
    satirlar.append(f"## {KATEGORI_ADI[kat]} ({len(dersler)} konu)")
    satirlar.append(f"")
    if kat in hub_aciklamalari:
        satirlar.append(f"{hub_aciklamalari[kat]}")
        satirlar.append(f"")
    satirlar.append(f"Hub: {BASE}/dersler/{kat}/")
    satirlar.append(f"")

    for ders in dersler:
        satirlar.append(f"### {ders['baslik']}")
        satirlar.append(f"URL: {ders['url']}")
        if ders["aciklama"]:
            satirlar.append(f"{ders['aciklama']}")
        if ders["lead"]:
            satirlar.append(f"")
            satirlar.append(f"{ders['lead']}")
        if ders["h2"]:
            satirlar.append(f"")
            satirlar.append("Alt başlıklar:")
            for h in ders["h2"]:
                satirlar.append(f"- {h}")
        satirlar.append(f"")

# Ek kaynaklar
satirlar.append("---")
satirlar.append("")
satirlar.append("## Ek Kaynaklar")
satirlar.append("")
satirlar.append(f"- Hap Bilgiler (76 kısa özet): {BASE}/hap-bilgiler/")
satirlar.append(f"- Soru Çöz: {BASE}/ehliyet-sinav-sorulari/")
satirlar.append(f"- Deneme Sınavı (giriş gerektirmez, 50 soru / 45 dk): {BASE}/deneme-sinavi/")
for _k, _a in (("ilk-yardim", "İlk Yardım"), ("trafik-ve-cevre", "Trafik ve Çevre"), ("arac-teknigi", "Araç Tekniği"), ("trafik-adabi", "Trafik Adabı")):
    satirlar.append(f"- {_a} çıkmış sorular: {BASE}/ehliyet-sinav-sorulari/{_k}/")
satirlar.append(f"- Ehliyet Nasıl Alınır: {BASE}/ehliyet-nasil-alinir/")
satirlar.append(f"- Sınav Konuları: {BASE}/ehliyet-sinav-konulari/")
satirlar.append(f"- Direksiyon Sınavı: {BASE}/direksiyon-sinavi/")
satirlar.append("")

hedef = ROOT / "llms-full.txt"
hedef.write_text("\n".join(satirlar), encoding="utf-8")
print(f"{sum(len(d) for d in kategoriler.values())} ders -> {hedef.relative_to(ROOT)}")
