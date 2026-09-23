# ehliyet.digital MCP Server

Turkiye B sinifi surucu belgesi (ehliyet) sinavina hazirlik verilerini AI ajanlarina sunan [Model Context Protocol](https://modelcontextprotocol.io/) sunucusu.

## Veri kaynaklari

| Dosya | Icerik |
|---|---|
| `data/questions.json` | 200 soru (4 deneme sinavi) |
| `data/quick-facts.json` | 80 hap bilgi |
| `data/lesson-summaries.json` | 43 ders, 354 atomik bilgi |

Veri dosyalari `tools/mcp-veri-uret.py` ile sitedeki JS ve HTML kaynaklarindan uretilir.

## Kurulum

```bash
cd mcp
pip install -r requirements.txt
```

## Calistirma

```bash
python server.py
```

Sunucu stdio uzerinden MCP protokoluyle iletisim kurar.

### Claude Desktop yapilandirmasi

`claude_desktop_config.json` dosyasina ekleyin:

```json
{
  "mcpServers": {
    "ehliyet-digital": {
      "command": "python",
      "args": ["/tam/yol/ehliyet-main/mcp/server.py"]
    }
  }
}
```

### Claude Code yapilandirmasi

`.claude/settings.json` dosyasina ekleyin:

```json
{
  "mcpServers": {
    "ehliyet-digital": {
      "command": "python",
      "args": ["/tam/yol/ehliyet-main/mcp/server.py"]
    }
  }
}
```

## Araclar (Tools)

### 1. `get_practice_questions`

Belirtilen bolumden rastgele sorular dondurur.

| Parametre | Tur | Zorunlu | Aciklama |
|---|---|---|---|
| `section` | string | Evet | `ilk_yardim`, `trafik_ve_cevre`, `arac_teknigi`, `trafik_adabi` veya `all` |
| `count` | integer | Hayir | Soru sayisi (varsayilan: 5, maks: 50) |

### 2. `get_quick_facts`

Hap bilgileri (kisa ozetler) dondurur.

| Parametre | Tur | Zorunlu | Aciklama |
|---|---|---|---|
| `section` | string | Evet | Bolum adi (yukardaki enum) |

### 3. `generate_mock_exam`

50 soruluk deneme sinavi olusturur. Gercek sinav dagitimiyla ayni: 12 Ilk Yardim, 23 Trafik ve Cevre, 9 Arac Teknigi, 6 Trafik Adabi.

Parametre almaz.

### 4. `get_lesson_summary`

Belirli bir ders icin atomik bilgileri dondurur.

| Parametre | Tur | Zorunlu | Aciklama |
|---|---|---|---|
| `section` | string | Evet | Bolum adi |
| `topic` | string | Hayir | Ders konusu (kismi eslesme: "kanama", "hiz", "fren") |

### 5. `explain_answer`

Soru ID'sine gore dogru cevabi, ilgili hap bilgileri ve ders linklerini dondurur.

| Parametre | Tur | Zorunlu | Aciklama |
|---|---|---|---|
| `question_id` | string | Evet | Soru ID'si (ornek: `sinav1-q01`) |

## REST API (alternatif)

MCP yerine dogrudan HTTP ile de erisebilirsiniz:

```
GET https://ehliyet.digital/api/questions?section=ilk_yardim&count=5
GET https://ehliyet.digital/api/quick-facts?section=trafik_ve_cevre
GET https://ehliyet.digital/api/mock-exam
GET https://ehliyet.digital/api/lesson-summary?section=arac_teknigi&topic=fren
```

Tum endpoint'ler JSON doner ve CORS aciktir — herhangi bir agent veya uygulama dogrudan kullanabilir.

## Remote MCP sunucusu (canlı)

Sunucu Railway'de host edilmektedir:

```
SSE endpoint: https://ehliyet-production.up.railway.app/sse
```

Claude Desktop yapilandirmasi (remote):

```json
{
  "mcpServers": {
    "ehliyet-digital": {
      "transport": "sse",
      "url": "https://ehliyet-production.up.railway.app/sse"
    }
  }
}
```

### Kendi sunucunuzda calistirmak icin

```bash
pip install -r requirements.txt
python server.py --http --port 8080
```

## Ornek kullanim

Bir AI ajanina:

- "Bana 10 tane Ilk Yardim sorusu sor" → `get_practice_questions(section="ilk_yardim", count=10)`
- "Trafik levhalari hakkinda hap bilgiler ver" → `get_quick_facts(section="trafik_ve_cevre")`
- "Deneme sinavi olustur" → `generate_mock_exam()`
- "Kanamalar konusunu ozetle" → `get_lesson_summary(section="ilk_yardim", topic="kanamalar")`
- "sinav2-q05 sorusunu acikla" → `explain_answer(question_id="sinav2-q05")`

## Veri guncelleme

Sitedeki sorular veya ders notlari degistiyse:

```bash
python tools/mcp-veri-uret.py
```

Bu komut `mcp/data/` altindaki JSON dosyalarini yeniden olusturur.
