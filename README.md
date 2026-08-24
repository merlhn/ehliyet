# ehliyet.digital

**Türkiye ehliyet (sürücü belgesi) sınavına ücretsiz hazırlık platformu.**

MEB MTSK müfredatına uygun 43 ders notu, 76 hap bilgi, 200 çıkmış sınav sorusu ve gerçek formatta deneme sınavları. Reklamsız, açık kaynak.

🌐 **Site:** [ehliyet.digital](https://ehliyet.digital)
📄 **LLM dizini:** [llms.txt](https://ehliyet.digital/llms.txt) · [llms-full.txt](https://ehliyet.digital/llms-full.txt)
🔌 **MCP:** [ehliyet-production.up.railway.app/mcp](https://ehliyet-production.up.railway.app/mcp) · [MCP Market](https://mcpmarket.com/server/ehliyet-digital) · [Smithery](https://smithery.ai/servers/omerlhn/ehliyet-digital) · MCP Registry: `io.github.merlhn/ehliyet-digital`

---

## Ne içerir?

| İçerik | Adet | Açıklama |
|--------|------|----------|
| Ders notları | 43 | 4 kategoride sınav odaklı konu anlatımı |
| Hap bilgiler | 76 | Tek cümlelik ezberlenecek kurallar |
| Atomik özetler | ~560 | Her ders sayfasında makine-okunur bilgi satırları |
| Sınav soruları | 200 | 4 deneme sınavından çıkmış sorular + cevaplar |
| Bireysel soru sayfaları | 186 | Her soru kendi URL'inde, cevap + açıklama ile |
| Bireysel hap bilgi sayfaları | 76 | Her hap bilgi kendi URL'inde, bağlam + ilgili ders ile |

### Ders kategorileri

| Kategori | Konu sayısı | Sınav dağılımı |
|----------|-------------|----------------|
| İlk Yardım | 12 | 12 soru (%24) |
| Trafik ve Çevre Bilgisi | 11 | 23 soru (%46) |
| Araç Tekniği (Motor) | 15 | 9 soru (%18) |
| Trafik Adabı | 5 | 6 soru (%12) |

### Sınav formatı

- 50 soru, 45 dakika
- Her doğru cevap 2 puan, yanlış doğruyu götürmez
- Geçme notu: 70 puan (en az 35 doğru)

---

## API

Tüm verilere programatik erişim — CORS açık, kimlik doğrulama yok.

### REST API (Vercel)

```bash
# 5 rastgele İlk Yardım sorusu
curl "https://ehliyet.digital/api/questions?section=ilk_yardim&count=5"

# Trafik ve Çevre hap bilgileri
curl "https://ehliyet.digital/api/quick-facts?section=trafik_ve_cevre"

# 50 soruluk deneme sınavı (gerçek dağılımla)
curl "https://ehliyet.digital/api/mock-exam"

# Fren sistemi ders özeti
curl "https://ehliyet.digital/api/lesson-summary?section=arac_teknigi&topic=fren"
```

**Endpoint'ler:**

| Endpoint | Parametreler | Açıklama |
|----------|-------------|----------|
| `/api/questions` | `section`, `count` | Rastgele soru döner |
| `/api/quick-facts` | `section` | Hap bilgiler |
| `/api/mock-exam` | — | 50 soruluk tam deneme |
| `/api/lesson-summary` | `section`, `topic` | Ders atomik özeti |

`section` değerleri: `ilk_yardim`, `trafik_ve_cevre`, `arac_teknigi`, `trafik_adabi`, `all`

### Örnek yanıt

```json
{
  "count": 1,
  "section": "ilk_yardim",
  "source": "ehliyet.digital",
  "questions": [
    {
      "id": "sinav1-q02",
      "exam": "Sınav 1",
      "section": "İlk Yardım",
      "stem": "Yetişkinlerde temel yaşam desteği ile ilgili uygulamalardan hangisi doğrudur?",
      "options": [
        "A) Göğüs kemiği 3 cm aşağı inecek şekilde bası yapılması",
        "B) Temel yaşam desteğine yapay solunum ile başlanması",
        "C) 30 kalp masajı, 2 yapay solunum şeklinde uygulanması",
        "D) Kalp masajı hızının dakikada 30 bası olacak şekilde ayarlanması"
      ],
      "correct_index": 2,
      "correct_letter": "C",
      "correct_text": "30 kalp masajı, 2 yapay solunum şeklinde uygulanması",
      "has_image": false
    }
  ]
}
```

---

## MCP Sunucusu

AI agent'lar Model Context Protocol ile doğrudan bağlanabilir.

**Remote (canlı):**
```
Streamable HTTP: https://ehliyet-production.up.railway.app/mcp   (önerilen)
SSE (eski):      https://ehliyet-production.up.railway.app/sse
```

**Claude Desktop yapılandırması:**
```json
{
  "mcpServers": {
    "ehliyet-digital": {
      "type": "http",
      "url": "https://ehliyet-production.up.railway.app/mcp"
    }
  }
}
```

**Lokal çalıştırma:**
```bash
cd mcp
pip install -r requirements.txt
python server.py          # stdio (Claude Desktop/Code)
python server.py --http   # HTTP/SSE (remote agent'lar)
```

**Araçlar:**

| Araç | Açıklama |
|------|----------|
| `get_practice_questions(section, count)` | Rastgele soru döner |
| `get_quick_facts(section)` | Hap bilgiler |
| `generate_mock_exam()` | 50 soruluk deneme sınavı |
| `get_lesson_summary(section, topic)` | Ders atomik özeti |
| `explain_answer(question_id)` | Soru açıklaması + ilgili dersler |

---

## Veri dosyaları

Makine-okunur JSON formatında:

| Dosya | İçerik |
|-------|--------|
| [`mcp/data/questions.json`](mcp/data/questions.json) | 200 soru (4 sınav) |
| [`mcp/data/quick-facts.json`](mcp/data/quick-facts.json) | 76 hap bilgi |
| [`mcp/data/lesson-summaries.json`](mcp/data/lesson-summaries.json) | 43 ders, ~560 atomik bilgi |

---

## Teknoloji

- **Frontend:** Statik HTML/CSS/JS — build adımı yok, SSR
- **Hosting:** Vercel (site) + Railway (MCP)
- **Auth:** Firebase (Google OAuth)
- **Veritabanı:** Firestore (yalnızca kullanıcı profili ve sınav sonuçları)
- **Analytics:** GA4 (custom event'ler: sign_up, login, exam_start, exam_complete, exam_abandon, feedback_submit)

---

## Yerelde çalıştırma

```bash
python3 -m http.server 8000
# http://localhost:8000
```

---

## Proje yapısı

```
├── index.html                  Ana sayfa
├── dersler/                    43 ders notu (4 kategori)
├── hap-bilgiler/               76 hap bilgi (4 kategori)
├── ehliyet-sinav-sorulari/     20 örnek soru
├── soru/                       186 bireysel soru sayfası
├── panel/                      Giriş gerektiren alan (sınavlar)
├── api/                        REST API (Vercel serverless)
├── mcp/                        MCP sunucusu + veri dosyaları
├── assets/js/questions-*.js    Soru bankaları (4 sınav)
├── tools/                      Üretici scriptler
│   ├── schema-uret.py          JSON-LD yapısal veri
│   ├── sitemap-uret.py         sitemap.xml
│   ├── llms-uret.py            llms-full.txt
│   ├── feed-uret.py            RSS feed + discovery link
│   ├── soru-sayfa-uret.py      Bireysel soru sayfaları
│   ├── hap-sayfa-uret.py       Bireysel hap bilgi sayfaları
│   ├── atomik-ekle.py          Ders atomik özetleri
│   ├── cevap-ac.py             Soru cevaplarını HTML'e taşı
│   └── mcp-veri-uret.py        MCP JSON veri dosyaları
├── llms.txt                    AI/LLM site dizini
├── llms-full.txt               Detaylı içerik dizini
├── feed.xml                    RSS feed
├── sitemap.xml                 251 URL
├── robots.txt                  AI tarayıcıları açık
└── 404.html                    Özel hata sayfası
```

---

## İçerik kaynakları

- MEB Motorlu Taşıt Sürücüleri Kursu (MTSK) müfredatı
- 2918 sayılı Karayolları Trafik Kanunu ve ilgili yönetmelikler
- Türkiye Kızılay Derneği ilk yardım eğitim materyalleri
- Gerçek MTSK e-sınavlarında çıkmış sorular

---

## Lisans

Bu proje açık kaynak olarak yayınlanmıştır. İçerikler MEB MTSK müfredatından derlenmiştir.

---

## İletişim

- **Site:** [ehliyet.digital](https://ehliyet.digital)
- **Hakkında:** [ehliyet.digital/hakkinda](https://ehliyet.digital/hakkinda/)
- **GitHub:** [github.com/merlhn/ehliyet](https://github.com/merlhn/ehliyet)
- **MCP Market:** [mcpmarket.com/server/ehliyet-digital](https://mcpmarket.com/server/ehliyet-digital)
- **Smithery:** [smithery.ai/servers/omerlhn/ehliyet-digital](https://smithery.ai/servers/omerlhn/ehliyet-digital)
- **MCP Registry:** `io.github.merlhn/ehliyet-digital`
