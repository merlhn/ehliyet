# Backlog

Açık işler ve bekleyen kararlar. Tamamlananlar en alta taşınır.

---

## Sıradaki

### 1. Analitik çerezleri için onay (KVKK) — karar bekliyor
GA4 343 sayfada onay alınmadan yükleniyor ve `_ga` çerezi yazıyor. Gizlilik metni bunu
artık açıkça söylüyor ve hukuki sebep olarak meşru menfaat gösteriyor; ancak KVKK
Kurumu'nun çerez rehberi analitik çerezler için açık rıza bekliyor. Seçenekler:

- Çerez onay bandı: onaydan önce GA yüklenmez (Consent Mode ile)
- GA4'ü kaldırıp çerezsiz bir ölçüm aracına geçmek
- Bugünkü hâliyle bırakıp riski kabul etmek

Aynı başlıkta: Firebase Authentication, Google Analytics ve Vercel verileri yurt
dışında işleniyor (KVKK m. 9). Metin aktarımı belirtiyor; aktarımın dayanağı
(standart sözleşme vb.) bir hukukçuya sorulmalı.

### 2. Yapay zekâ görünürlüğü (Bing + ölçüm)
- **Bing Webmaster Tools:** Search Console'dan içe aktararak siteyi ekle, sitemap'i gönder. ChatGPT arama ve Copilot Bing indeksini kullanır.
- **IndexNow:** her deploy'dan sonra `python3 tools/indexnow.py` (son commit'te değişen sayfaları bildirir).
- **Aylık ölçüm:** Aşağıdaki soruları ChatGPT (arama açık), Perplexity, Gemini ve Google AI Overview'da sor; ehliyet.digital alıntılanıyor mu, not et.
  1. Ehliyet sınavında hangi dersten kaç soru çıkar?
  2. Ehliyet sınavını geçmek için kaç doğru gerekir?
  3. Ücretsiz ehliyet deneme sınavı nerede çözülür?
  4. Ehliyet çıkmış sorular 2026
  5. Teskereci yöntemi nedir?
  6. Ayak frenine basınca hangi tekerlekler durur?
  7. Şok pozisyonunda ayaklar kaç cm kaldırılır?
  8. Aralıklı yanıp sönen kırmızı ışık ne anlama gelir?
  9. Kavşakta ilk geçiş hakkı kimindir?
  10. 2026 ehliyet ücreti ne kadar?
  11. Ehliyet sınavı hap bilgiler
  12. İlk yardımın ABC'si nedir?
- **Dış anılma:** Ekşi Sözlük / Reddit ehliyet başlıklarına faydalı cevap, sürücü kursu blog iş birlikleri, açık API'nin Türkçe veri seti listelerine eklenmesi.

### 3. MCP sunucusunu Google Cloud Run'a taşı
Railway'deki sunucu kapandı (1 Eki 2026'da tüm yollar "Application not found" dönüyor).
README, `llms.txt`, `server.json`, Smithery, MCP Market ve MCP Registry hâlâ eski
adresi gösteriyor; o zamana kadar dizinlerdeki kayıtlar ölü.

Hazır olanlar: `mcp/` imajı değişiklik gerektirmiyor (8080, durumsuz); Docker'da yerelde
denendi, beş araç çalışıyor. `gcloud` kuruldu (`brew install --cask gcloud-cli`).

Kalanlar:
- `gcloud auth login` — Firebase projesinin (`ehliyet-52d4d`) sahibi hesapla
- Projeyi Blaze planına geçir (Cloud Run faturalandırma hesabı ister); 1 $ bütçe uyarısı kur
- `gcloud run deploy ehliyet-mcp --source mcp --region europe-west1 --allow-unauthenticated
  --min-instances 0 --max-instances 1 --memory 256Mi` — tek instance SSE'nin
  (`/sse` + `/messages/`) aynı makineye düşmesini de garanti eder
- Canlıda initialize / tools/list / tools/call testi
- Alan adı kararı: `*.run.app` adresi mi, `mcp.ehliyet.digital` mı (DNS'e tek kayıt;
  servis bir daha değişirse dizin kayıtları bozulmaz)
- Eski adresi değiştir: `server.json`, `README.md`, `mcp/README.md`, `llms.txt`
  (5 × `/mcp`, 5 × `/sse`); ardından Smithery, MCP Market ve MCP Registry kayıtları

## Sonraki faz

### Ödeme
Sınav 1 ücretsiz, diğerleri ücretli olacaktı; sağlayıcı seçilmedi. Yetki kayıtları
(`users/{uid}/yetkiler/{sinavId}`) yalnızca sunucu tarafında yazılır; istemcinin
yazması Firestore kurallarıyla engelli.

Ödemeden önce çözülmesi gerekenler:
- **Soru bankaları herkese açık.** `assets/js/questions-N.js` ve açık deneme sınavı
  (`/deneme-sinavi/`) bilinçli olarak giriş istemiyor; ücretli içerik gelirse bu
  dosyalar public klasörden çıkar ve `/api/sorular?sinav=N` → Firebase ID token
  doğrula → yetki kontrol et → JSON dön akışına geçilir (repoya `package.json` girer).
- **Hesap silme sunucuya taşınır.** İstemci `yetkiler` alt koleksiyonunu silemez;
  yetki yazılmaya başlayınca silme Admin SDK'lı bir uca (`/api/hesap-sil`) geçmeli.
- Gizlilik metnine ödeme sağlayıcısı ve fatura verileri eklenir.

### Sınav 5 ve sonrası
Sınav 1–4 yayında. Akış `README.md` içinde. `../Sınav_N/` klasöründen
`assets/js/questions-N.js` + `panel/sinav-N/` üretilir. Cevaplar yayına alınmadan önce
anahtarla programatik doğrulanmalı.

---

## Bilinen kabuller

**Sınav puanı istemcide hesaplanıyor.** Teknik bilgisi olan biri sahte sonuç yazabilir.
Veri kişisel ilerleme takibi olduğu için şimdilik kabul edilebilir. Sıralama, rozet
veya sertifika gibi rekabetçi bir özellik eklenirse puanlama sunucuya taşınmalı.

**Gizli sayfa ≠ erişim kontrolü.** `noindex` ve link vermemek sayfayı aramadan ve
gezinmeden çıkarır, ama linke sahip olan herkes açar.

**Panel çok sayfalı kalıyor, SPA'ya geçilmeyecek.** Her tıklama tam sayfa geçişi
olduğu için belge, CSS, font ve Firebase yeniden kuruluyor; ölçümde ~172ms ana
iş parçacığı bloklaması görünüyor. Sayfa kendisi hafif (21KB HTML, 121 DOM
düğümü, render 0.6ms), yani yük bizim kodumuzdan değil gezinmenin kendisinden
geliyor. SPA bunu bitirirdi ama URL yönetimini (geri tuşu, paylaşma, yenileme)
elle kurmayı gerektirir; kazanç şu aşamada bu maliyeti karşılamıyor.
Değerlendirildi ve bilinçli olarak reddedildi. Sınav sonucunu panelde gösterme
gibi bir akış geldiğinde yeniden bakılabilir.

**Geri bildirimler hesap silmeyle silinmez.** `feedback` koleksiyonunu istemci okuyamaz,
dolayısıyla silemez. Gizlilik metni bunu söylüyor; talep gelirse Console'dan elle silinir.

---

## Tamamlananlar

- Sınav 2 eklendi (50 soru, cevap anahtarıyla doğrulandı, 38 medya dosyası)
- Klasör yapısı yeniden düzenlendi: `/dersler/` ve `/deneme-sinavlari/` kardeş bölümler
  (`/deneme-sinavlari/` sonradan `/ehliyet-sinav-sorulari/`'na yönlendirildi),
  varlıklar `/assets/` altında, URL'ler kebab-case ve ASCII
- Proje `ehliyet.digital` olarak adlandırıldı, Vercel'e deploy edildi
- Firebase kuruldu: Google girişi, Firestore (`eur3`), güvenlik kuralları
- Header'a Google ile giriş butonu ve profil menüsü
- `ehliyet.digital` alan adı bağlandı; www kalıcı olarak apex'e yönleniyor
- Header düzeni içerik kutusuyla hizalandı, mobil sıkışma giderildi
- Giriş sonrası panel (`/panel/`): yan menü, üst bar, deneme sınavları listesi
- Sınav ve kılavuz sayfaları panelin içine taşındı (`/panel/sinav-N/`); giriş zorunlu,
  sınav sürerken menüden ayrılmak onay istiyor

---
- Google giriş ekranında kendi alan adı: `authDomain: 'ehliyet.digital'` + `/__/auth/*`
  proxy'si (Vercel rewrite)
- OAuth onay ekranı kimliği (ad, logo, ana sayfa, gizlilik ve şartlar bağlantıları)
- Panel: Profilim (ad, soyad, telefon, ehliyet türü), Ayarlar (hesap bilgileri, hesabı
  sil), sınav geçmişi, genel performans ve çalışılacak konular
- Sınav sonucu kaydı: dört panel sınavı ve açık deneme (girişliyken)
  `users/{uid}/denemeler`'e yazıyor
- Logo: panelde ve public header'da marka, favicon seti (`tools/favicon-uret.py`)
- Geri bildirim gerçekten gönderiliyor: Firestore `feedback` koleksiyonu
- Sınav 3 ve 4 eklendi
- Bing Site Scan (1 Eki 2026): 8 kırık link (tipografik tırnaklı `href`), 5 sayfada
  boş `alt`, 211 uzun başlık düzeltildi; `tools/html-kontrol.py` yayından önce yakalar
- Gizlilik metni KVKK aydınlatma metni olarak yeniden yazıldı (1 Eki 2026): Google
  girişi, profil, sonuçlar, geri bildirim, GA4, Vercel, yurt dışı aktarım, saklama,
  silme, m. 11 hakları; kullanım şartları ve hakkında sayfası buna uyduruldu
- Hesap silme düzeltildi: önce Google ile yeniden doğrulama, sonra denemeler, profil ve
  Auth hesabı; kurallar 1 Eki 2026'da yayında, canlıda denendi
- Hap bilgi kategori sayfaları Google Fonts yerine yerel fontlara geçti; `hap-uret.py`
  çıktısı canlı sayfalarla birebir

---

## İptal edilenler

- **Deneme sınavlarının PDF olarak indirilmesi.** Video içeren sorular kağıda
  aktarılamadığı için gizli bir video alanı (`/v/<sinav>/<soru>/`) kurulmuştu;
  PDF işi iptal edilince o sayfalar da silindi.
