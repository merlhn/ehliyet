#!/usr/bin/env python3
"""
Başlıklardaki yılı yeniler (ör. 1 Ocak'ta "2026" -> "2027").

Kullanım (depo kökünden):
    python3 tools/yil-guncelle.py 2026 2027            # kuru çalıştırma: ne değişecek, listeler
    python3 tools/yil-guncelle.py 2026 2027 --uygula   # dosyalara yazar

Yalnızca "güncellik" işareti olan yerlere dokunur: <title>, og:title, twitter:title,
<h1> ve JSON-LD "headline". Gövde metnine, tarihlere ("Eylül 2026", ISO tarihler) ve
tutar tablolarına dokunmaz.

VERI_SAYFALARI hariç tutulur: oradaki yıl bir tarifeyi anlatır (ör. 2026 harçları);
yeni yılın rakamları girilmeden başlığa yeni yıl yazmak yanlış bilgi olur. O sayfalar
yeni tutarlarla elle güncellendikten sonra --veri ile bu araçtan geçirilebilir.

Üreticilerde yıl geçen başlık kalıpları KAYNAK_KALIPLARI'nda; araç onları da yeniler,
ardından ilgili üreticiler (hap-uret, hap-sayfa-uret, schema-uret, feed-uret,
banner-ekle, sitemap-uret, llms-uret) çalıştırılmalıdır.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HARIC = (".git", ".claude", "panel", "mcp", "node_modules", "tools")
# Ücret içeren sayfalar: ehliyet-nasil-alinir ve direksiyon-sinavi de 2026 tutarlarını anar.
VERI_SAYFALARI = {"ehliyet-fiyatlari", "ehliyet-nasil-alinir", "direksiyon-sinavi"}

# dosya -> yıl içeren başlık kalıpları ({y} yerine yıl gelir)
KAYNAK_KALIPLARI = {
    "tools/hap-uret.py": ["(Ehliyet {y})"],
    "tools/llms-uret.py": [],  # "Ehliyet Fiyatları {y}" veri sayfasıdır, --veri ile
}
VERI_KAYNAK_KALIPLARI = {
    "tools/llms-uret.py": ["Ehliyet Fiyatları {y}"],
}

ALANLAR = [
    re.compile(r"(<title>)(.*?)(</title>)", re.S),
    re.compile(r'(<meta property="og:title" content=")([^"]*)(")'),
    re.compile(r'(<meta name="twitter:title" content=")([^"]*)(")'),
    re.compile(r"(<h1[^>]*>)(.*?)(</h1>)", re.S),
    re.compile(r'("headline":\s*")([^"]*)(")'),
]


def yenile(metin, eski, yeni):
    # Yıl tek başına bir kelime olmalı; "2026-10-18" gibi tarihlere dokunma.
    desen = re.compile(r"(?<![\d-])" + eski + r"(?![\d-])")
    sayac = 0
    for alan in ALANLAR:
        def degistir(m):
            nonlocal sayac
            ic, n = desen.subn(yeni, m.group(2))
            sayac += n
            return m.group(1) + ic + m.group(3)
        metin = alan.sub(degistir, metin)
    return metin, sayac


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2 or not all(re.fullmatch(r"\d{4}", a) for a in args):
        raise SystemExit(__doc__)
    eski, yeni = args
    uygula, veri = "--uygula" in sys.argv, "--veri" in sys.argv

    toplam = 0
    for p in sorted(ROOT.rglob("index.html")):
        parcalar = p.relative_to(ROOT).parts
        if any(x in parcalar for x in HARIC):
            continue
        if parcalar[0] in VERI_SAYFALARI and not veri:
            continue
        s = p.read_text(encoding="utf-8")
        s2, n = yenile(s, eski, yeni)
        if n:
            toplam += n
            print(f"  {p.relative_to(ROOT)}: {n}")
            if uygula:
                p.write_text(s2, encoding="utf-8")

    kaliplar = dict(KAYNAK_KALIPLARI)
    if veri:
        for k, v in VERI_KAYNAK_KALIPLARI.items():
            kaliplar[k] = kaliplar.get(k, []) + v
    for dosya, liste in kaliplar.items():
        yol = ROOT / dosya
        s = yol.read_text(encoding="utf-8")
        s2 = s
        for k in liste:
            s2 = s2.replace(k.format(y=eski), k.format(y=yeni))
        if s2 != s:
            print(f"  {dosya}: kalıp yenilendi")
            toplam += 1
            if uygula:
                yol.write_text(s2, encoding="utf-8")

    print(f"{toplam} değişiklik" + ("" if uygula else " (kuru çalıştırma; yazmak için --uygula)"))
    if not veri:
        print("Not: " + ", ".join(sorted(VERI_SAYFALARI)) + " atlandı; yeni yıl tutarları girildikten sonra --veri ile çalıştır.")


if __name__ == "__main__":
    main()
