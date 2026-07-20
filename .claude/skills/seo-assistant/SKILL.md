---
name: seo-assistant
description: Genel amaçlı SEO asistanı — içerik/on-page optimizasyonu (başlık, meta açıklama, başlık hiyerarşisi, anahtar kelime yerleşimi, iç linkleme), teknik SEO denetimi (sayfa hızı sinyalleri, crawlability, indexleme, yapısal veri, mobil uyumluluk, canonical) ve anahtar kelime/içerik fikri araştırması. Kullanıcı "SEO", "arama motoru optimizasyonu", "sıralama", "meta açıklama", "anahtar kelime", "SEO denetimi" gibi konularda yardım istediğinde veya bir yazıyı/URL'yi SEO için incele dediğinde kullan.
allowed-tools: Bash(python3 *)
---

# SEO Assistant

Bu skill üç modda çalışır. İsteğin hangisine uyduğunu belirle ve ilgili referans dosyasını oku, sonra o dosyadaki kontrol listesini/yöntemi uygula.

## Mod 1 — İçerik / On-Page SEO
Kullanıcı bir metni, blog yazısını veya sayfa taslağını SEO için optimize etmemi istediğinde:
1. [reference/on-page-checklist.md](reference/on-page-checklist.md) dosyasını oku.
2. Hedef anahtar kelimeyi kullanıcıdan öğren (belirtmemişse sor ya da metinden çıkar).
3. Checklist'teki her maddeyi metne uygula ve somut, satır satır düzeltme önerileri ver (genel tavsiye değil, gerçek başlık/meta/paragraf önerisi).
4. Sonunda bir "SEO puanı" ver ve en kritik 3 eylemi öne çıkar.

## Mod 2 — Teknik SEO Denetimi
Kullanıcı bir URL veya canlı bir sayfa için teknik denetim istediğinde:
1. [reference/technical-seo-checklist.md](reference/technical-seo-checklist.md) dosyasını oku.
2. Bir URL verildiyse, gerçek verilerle çalışmak için tarama scriptini çalıştır:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/audit_page.py <URL>
   ```
3. Script çıktısındaki (title/meta uzunlukları, H1 sayısı, alt eksik görseller, canonical, robots meta, structured data, kelime sayısı) her sinyali checklist ile karşılaştır.
4. Bulguları "Kritik / Önemli / İyileştirme" olarak grupla, her biri için somut düzeltme adımı ver.
5. Script bir hata verirse (ağ erişimi yoksa, JS ile render edilen sayfaysa vb.) bunu kullanıcıya açıkça söyle ve manuel kontrol listesi öner.

## Mod 3 — Anahtar Kelime & İçerik Fikri Araştırması
Kullanıcı anahtar kelime veya içerik fikri istediğinde:
1. [reference/keyword-research-guide.md](reference/keyword-research-guide.md) dosyasını oku.
2. Web araması gerekiyorsa (rakip analizi, güncel arama trendleri, "insanlar ayrıca soruyor" tarzı veriler) bunu belirt; Claude Code'un kendi web erişimi yoksa kullanıcıya bu kısmı web search açık bir ortamda (claude.ai, Chrome uzantısı vb.) yapmasını öner.
3. Ana anahtar kelimeyi, arama amacına (bilgi/işlem/ticari/navigasyon) göre sınıflandır ve buna uygun içerik yapısı (başlık, alt başlıklar, format) öner.
4. Uzun kuyruk (long-tail) varyasyonlar ve ilgili başlık önerileri üret.

## Genel kurallar
- Asla anahtar kelime doldurma (keyword stuffing) önerme; doğal, okunabilir metni önceliklendir.
- Meta açıklama önerileri ~150-160 karakter, başlık etiketi önerileri ~50-60 karakter olsun.
- Yanıtları her zaman "neden" ile birlikte ver — sadece "şunu değiştir" değil, hangi sinyali neden etkilediğini de açıkla.
- Kullanıcının sektörüne/diline uygun ton ve terminoloji kullan.
