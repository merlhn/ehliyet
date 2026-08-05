#!/usr/bin/env python3
"""Soru bloklarındaki cevapları makine-okunur hale getirir.

Kullanım (depo kökünden):  python3 tools/cevap-ac.py

İki tür soru bloğunu işler:
1. /ehliyet-sinav-sorulari/ — <button class="soru-reveal">
2. Ders sayfalarındaki quiz — <button class="reveal-btn">

Her doğru cevabı (.sopt.correct veya .qo.correct) bulur ve butonun
yerine/yanına <details class="soru-cevap">/<summary> olarak ekler.

Idempotent: mevcut soru-cevap varsa tekrar eklemez.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

sayac = 0

for p in sorted(ROOT.rglob("index.html")):
    if any(x in p.relative_to(ROOT).parts for x in (".git", ".claude", "panel")):
        continue
    t = p.read_text(encoding="utf-8")
    if "soru-cevap" in t:
        continue  # zaten işlenmiş

    degisti = False

    # --- Tip 1: /ehliyet-sinav-sorulari/ — <button class="soru-reveal"> ---
    if "soru-reveal" in t:
        def soru_isle(m):
            global sayac
            blok = m.group(0)
            dogru = re.search(r'<div class="sopt correct"><span class="sl">([A-D]\))</span>\s*(.*?)</div>', blok)
            if not dogru:
                return blok
            harf = dogru.group(1)
            metin = re.sub(r"<[^>]+>", "", dogru.group(2)).strip()
            yeni = re.sub(
                r'<button class="soru-reveal"[^>]*>Cevabı Gör</button>',
                f'<details class="soru-cevap"><summary>Cevabı Gör</summary><p><b>Doğru cevap: {harf}</b> {metin}</p></details>',
                blok
            )
            if yeni != blok:
                sayac += 1
            return yeni

        t2 = re.sub(r'<div class="soru">.*?</div>\s*</div>\s*<button class="soru-reveal"[^>]*>.*?</button>\s*</div>',
                     soru_isle, t, flags=re.S)
        if t2 != t:
            t = t2
            degisti = True

    # --- Tip 2: Ders quizleri — <button class="reveal-btn"> ---
    if "reveal-btn" in t:
        # Her <li> içindeki doğru cevabı bul ve </li> öncesine details ekle
        def li_isle(m):
            global sayac
            li = m.group(0)
            dogru = re.search(r'<div class="qo correct"><span class="lbl">([A-D]\))</span>\s*(.*?)</div>', li)
            if not dogru:
                return li
            harf = dogru.group(1)
            metin = re.sub(r"<[^>]+>", "", dogru.group(2)).strip()
            ek = f'\n          <details class="soru-cevap"><summary>Cevabı Gör</summary><p><b>Doğru cevap: {harf}</b> {metin}</p></details>'
            li = li.rstrip()
            if li.endswith("</li>"):
                li = li[:-5] + ek + "\n        </li>"
                sayac += 1
            return li

        t2 = re.sub(r'<li>.*?</li>', li_isle, t, flags=re.S)
        if t2 != t:
            t = t2
            degisti = True

    if degisti:
        p.write_text(t, encoding="utf-8")
        print(f"  {p.relative_to(ROOT)}")

print(f"\n{sayac} cevap açıldı")
