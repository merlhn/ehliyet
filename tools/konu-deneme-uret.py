#!/usr/bin/env python3
"""/panel/konu-denemesi/index.html'i panel/sinav-1'deki sınav motorundan üretir.

?k=<kategori> ile dört sınavın o konudaki soruları tek denemede toplanır (süre soru
başına 54 sn, geçme %70). Giriş gerektirir (panel-kabuk.js); sonuç panele
kaydedilmez, panel istatistikleri 50 soruluk tam denemelere göre hesaplanıyor.

Kullanım (depo kökünden):  python3 tools/konu-deneme-uret.py
panel/sinav-1/index.html değiştiğinde tekrar çalıştırılır.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / 'panel/sinav-1/index.html').read_text(encoding='utf-8')

def degistir(metin, eski, yeni, adet=1):
    if metin.count(eski) != adet:
        sys.exit(f'BEKLENEN {adet} ESLESME, BULUNAN {metin.count(eski)}: {eski[:70]!r}')
    return metin.replace(eski, yeni)

html = degistir(html, '<title>MTSK E-Sınav Denemesi — Sınav 1</title>', '<title>Konu Denemesi — ehliyet.digital</title>')
html = degistir(html, '<div class="h-title">Sınav 1</div>', '<div class="h-title"></div>')
html = degistir(html, ": '/panel/'\">‹ Çıkış</button>", ": '/panel/?g=sinavlar'\">‹ Çıkış</button>")

# Dört soru dosyası sırayla yüklenir; her biri window.QUESTIONS'ı ezdiği için arada toplanır.
yukle = ''.join(
    f'<script src="/assets/js/questions-{n}.js"></script>\n'
    f'<script>{"window.TUM_SORULAR = window.QUESTIONS.slice();" if n == 1 else "window.TUM_SORULAR.push(...window.QUESTIONS);"}</script>\n'
    for n in (1, 2, 3, 4))
html = degistir(html, '<script src="/assets/js/questions-1.js"></script>\n', yukle)

html = degistir(html, "const Q = window.QUESTIONS;", """const KONULAR = {'ilk-yardim':'İlk Yardım','trafik-ve-cevre':'Trafik ve Çevre','arac-teknigi':'Araç Tekniği','trafik-adabi':'Trafik Adabı'};
const KONU = KONULAR[new URLSearchParams(location.search).get('k')] ? new URLSearchParams(location.search).get('k') : null;
if (!KONU) location.replace('/panel/?g=sinavlar');
const Q = KONU ? window.TUM_SORULAR.filter(q => q.section === KONULAR[KONU]) : [];""")
html = degistir(html, "const PASS_CORRECT = 35;         // 50 soruda geçme (≈70 puan)",
                      "const PASS_CORRECT = Math.ceil(Q.length * 0.7); // yüzde 70")
html = degistir(html, "const SINAV_ADI = 'Sınav 1';", """const SINAV_ADI = KONU ? KONULAR[KONU] + ' Denemesi' : '';
if (KONU) { document.title = SINAV_ADI + ' — ehliyet.digital'; document.querySelector('.h-title').textContent = SINAV_ADI; }""")
html = degistir(html, "const DURATION = 45*60;          // 45 dakika", "const DURATION = Q.length * 54;  // soru başına 54 sn")
html = degistir(html, "return {correct,wrong,empty,points:correct*2};",
                      "return {correct,wrong,empty,points:Math.round(correct/Q.length*100)};")
html = degistir(html, '<span class="qno">Soru ${q.n}</span>', '<span class="qno">Soru ${cur+1}</span>')

# "50 soru, her soru 2 puan" anlatımı konu denemesine uymaz.
i = html.index('      <p style="color:#444;max-width:660px')
j = html.index('</p>\n', i) + len('</p>\n')
html = html[:i] + html[j:]

# Sonuç kaydedilmez, analytics gider.
i = html.index("      await denemeKaydet(user.uid, {")
j = html.index("      });\n", i) + len("      });\n")
html = html[:i] + html[j:]
html = degistir(html, "      const { denemeKaydet } = await import('/assets/js/firebase.js');\n", "")

html = degistir(html, "kaynak:'panel', konu:''}); }", "kaynak:'panel', konu:KONU}); }")
html = degistir(html, "          kaynak: 'panel',\n          konu: ''\n", "          kaynak: 'panel',\n          konu: KONU\n")
html = degistir(html, "      kaynak: 'panel',\n      konu: ''\n", "      kaynak: 'panel',\n      konu: KONU\n")
html = degistir(html, "  location.href='index.html';\n", "  location.href='/panel/?g=sinavlar';\n")
html = degistir(html, "\nstartTimer();\nrender();\n", "\nif (KONU) { startTimer(); render(); }\n")

hedef = ROOT / 'panel/konu-denemesi/index.html'
hedef.parent.mkdir(exist_ok=True)
hedef.write_text(html, encoding='utf-8')
print('yazildi', hedef.relative_to(ROOT), len(html.splitlines()), 'satir')
