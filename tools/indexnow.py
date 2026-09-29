#!/usr/bin/env python3
"""Değişen sayfaları IndexNow ile Bing, Yandex ve diğer katılımcı arama
motorlarına bildirir. ChatGPT arama ve Copilot Bing indeksini kullandığı için
yeni/güncellenen sayfaların yapay zekâ asistanlarına hızlı ulaşmasını sağlar.

Deploy tamamlandıktan SONRA çalıştırılır (anahtar dosyası canlıda olmalı):
  python3 tools/indexnow.py                 # son commit'te değişen sayfalar
  python3 tools/indexnow.py --son 3         # son 3 commit'te değişenler
  python3 tools/indexnow.py --hepsi         # sitemap'teki tüm adresler
  python3 tools/indexnow.py --kuru ...      # göndermeden listele

Anahtar, depo kökündeki <anahtar>.txt dosyasıdır (içeriği dosya adıyla aynı).
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "ehliyet.digital"
BASE = f"https://{HOST}"
UC_NOKTA = "https://api.indexnow.org/indexnow"
PARTI = 10000  # protokolün tek istekte izin verdiği en fazla adres


def anahtar_bul():
    for p in ROOT.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", p.stem) and p.read_text().strip() == p.stem:
            return p.stem
    sys.exit("IndexNow anahtar dosyası bulunamadı (<32 hex>.txt).")


def sitemap_adresleri():
    return re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


def degisen_adresler(son):
    cikti = subprocess.run(["git", "diff", "--name-only", f"HEAD~{son}", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.split()
    gecerli = set(sitemap_adresleri())
    adresler = []
    for yol in cikti:
        if not yol.endswith("index.html"):
            continue
        url = f"{BASE}/{yol[:-len('index.html')]}"
        if url in gecerli:  # silinen, noindex ya da sitemap dışı sayfalar gönderilmez
            adresler.append(url)
    return sorted(set(adresler))


def gonder(anahtar, adresler):
    for i in range(0, len(adresler), PARTI):
        govde = json.dumps({
            "host": HOST,
            "key": anahtar,
            "keyLocation": f"{BASE}/{anahtar}.txt",
            "urlList": adresler[i:i + PARTI],
        }).encode()
        istek = urllib.request.Request(UC_NOKTA, data=govde, method="POST",
                                       headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(istek, timeout=30) as yanit:
            print(f"IndexNow: {len(adresler[i:i + PARTI])} adres -> HTTP {yanit.status}")


def main():
    args = sys.argv[1:]
    kuru = "--kuru" in args
    if "--hepsi" in args:
        adresler = sitemap_adresleri()
    else:
        son = int(args[args.index("--son") + 1]) if "--son" in args else 1
        adresler = degisen_adresler(son)
    if not adresler:
        print("Bildirilecek sayfa yok.")
        return
    for a in adresler:
        print(" ", a)
    if kuru:
        print(f"{len(adresler)} adres (kuru çalıştırma, gönderilmedi)")
        return
    gonder(anahtar_bul(), adresler)


if __name__ == "__main__":
    main()
