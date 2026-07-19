# ehliyet.digital

Ehliyet (MTSK) sınavına hazırlık sitesi. İki ana bölüm var: **ders notları** ve **deneme sınavları**.

Build adımı yok — tamamen statik HTML/CSS/JS. Herhangi bir statik sunucudan servis edilir.

## Yerelde çalıştırma

```bash
python3 -m http.server 8000
```

Ardından http://localhost:8000

## Klasör yapısı

```
index.html                          açılış sayfası
dersler/                            ders listesi (hub)
  <konu>/<slug>/index.html          43 ders notu
deneme-sinavlari/                   sınav listesi (hub)
  sinav-N/index.html                testin kendisi
  sinav-N/kilavuz/index.html        sınavın giriş kapısı
assets/
  js/questions-N.js                 sınav soru bankaları
  js/lessons-nav.js                 ders sıralaması + sayfa içi içindekiler
  js/search-index.js                site içi arama verisi
  js/feedback.js
  css/kilavuz.css
  kilavuz-govde.html                kılavuz metni (tüm sınavlarda ortak)
  img/sinav-N/                      sınav görselleri ve videoları
hakkinda/ iletisim/ gizlilik/ kullanim-sartlari/
```

## Konvansiyonlar

- **URL'ler kebab-case ve ASCII.** Türkçe karakter kullanılmaz; tarayıcı bunları yüzde-kodlar ve paylaşımda sorun çıkarır.
- **Ders numarası URL'de yer almaz.** Sıralama `assets/js/lessons-nav.js` içindeki `COURSES` dizisinden gelir; böylece araya ders eklendiğinde URL'ler değişmez.
- **Kılavuz metni tek kaynaktadır.** Her sınavın kılavuz sayfası `assets/kilavuz-govde.html` dosyasını çeker; sınav sayısı artınca metin çoğalmaz.

## Hesap ve veritabanı

Firebase projesi `ehliyet-52d4d`; giriş yalnızca Google ile, veritabanı Firestore (`eur3`).
Veritabanında **içerik tutulmaz** — sadece profil, sınav sonuçları ve sınav yetkileri.

- `assets/js/firebase.js` — başlatma ve veri yardımcıları. İçindeki config değerleri gizli değildir; erişimi koruyan şey `firestore.rules` ve sunucu tarafındaki yetki kontrolüdür.
- `firestore.rules` — kullanıcı yalnızca kendi verisine erişir. **Yetki kayıtlarına istemci yazamaz**; yazma yalnızca Admin SDK ile sunucu tarafında yapılır. Kurallar konsolda `Firestore → Rules` altından yayınlanır.
- `vercel.json` — `/__/auth/*` isteklerini Firebase'e proxy'ler. Bu rewrite, `firebaseConfig.authDomain` değerinin `ehliyet.digital` olabilmesi için **zorunludur**; olmazsa Google giriş ekranında `ehliyet-52d4d.firebaseapp.com` yazar. İkisi birlikte değiştirilmeli, tek başına biri girişi kırar.

## Yeni ders ekleme

`ders-notu` agent'ı kullanılır (`.claude/agents/ders-notu.md`). Üç yere kayıt gerekir: ana sayfa akordeonu, `lessons-nav.js` ve `search-index.js`.

## Yeni deneme sınavı ekleme

Kaynaklar `../Sınav_N/` altında toplanır (soru ekran görüntüleri, soru materyalleri, cevap anahtarı PDF'i); bunlardan `assets/js/questions-N.js` ve `deneme-sinavlari/sinav-N/` üretilir. Cevaplar yayına alınmadan önce anahtarla programatik olarak karşılaştırılmalıdır.

## SEO ve ölçümleme

- `robots.txt` — `/panel/` hariç her şey taranabilir, sitemap'i işaret eder.
- `sitemap.xml` — **elle düzenlenmez.** Ders ya da sınav eklendikten sonra
  `python3 tools/sitemap-uret.py` çalıştırılır; script `index.html` dosyalarını
  tarar, `panel/` ve `noindex` işaretli sayfaları atlar, `lastmod` değerini son
  commit tarihinden alır.
- **GA4 etiketi her sayfanın `<head>`'inde inline durur**, ayrı bir js dosyasında
  değil. Sebebi: Search Console'un Analytics ile doğrulama yöntemi sayfanın ham
  HTML'ine bakar, JavaScript çalıştırmaz — etiket dinamik yüklenirse doğrulama
  başarısız olur. Ölçüm kimliği değişirse 55 dosyada birden değiştirilir:

  ```bash
  grep -rl 'G-34HL041XN0' --include='*.html' . | xargs sed -i '' 's/G-34HL041XN0/G-YENIID/g'
  ```

## Favicon

Kaynak `assets/img/marka/logo.png`. Üretilen dosyalar (`favicon.ico`,
`apple-touch-icon.png`, `icon-192.png`, `icon-512.png`) **elle düzenlenmez**;
logo değişirse `python3 tools/favicon-uret.py` tekrar çalıştırılır.

Logo şeffaf zeminde ve neredeyse siyah; olduğu gibi kullanılsaydı tarayıcının
koyu tema sekme şeridinde kaybolurdu. Bu yüzden beyaz yuvarlatılmış bir zemine
oturtuluyor — kontrastı döşemenin kendisi sağlıyor.

İnce çizgili kart detayı 16px'te okunmuyor; bu logonun doğasından ve kabul
edilmiş bir sınır. 32px ve üstünde sorun yok. Keskinlik istenirse çözüm
favicon'a özel sadeleştirilmiş bir işaret çizmek olur.

## Kural: giriş sonrası hiçbir sayfa indekslenmez

Kullanıcı giriş yaptıktan sonra gördüğü hiçbir sayfa arama sonuçlarında yer
almaz. Üç katman birden gerekir:

1. sayfada `<meta name="robots" content="noindex">`
2. `robots.txt` içinde dizin `Disallow`
3. `sitemap.xml` içinde adres bulunmaması

Üçü de gerekli. **robots.txt tek başına yetmez** — o yalnızca taramayı
engeller, indekslemeyi değil; sayfaya dışarıdan link verilirse Google adresi
yine listeleyebilir. İndekslemeyi durduran şey `noindex` etiketidir.

`python3 tools/index-kontrol.py` bu üç katmanı doğrular ve ihlal varsa 1 ile
çıkar. Yeni kapılı sayfa eklendikten sonra çalıştırılır. Yeni bir yetki
mekanizması gelirse script içindeki `KAPI_ISARETLERI` listesine eklenmeli,
yoksa kontrol o sayfayı gözden kaçırır.

## Meta açıklama ve paylaşım önizlemesi

Her genel sayfada `<title>` → `meta description` → `canonical` → Open Graph
bloğu sırası korunur. OG alanları açıklama ve canonical'dan türetilir; `og:url`
ile `canonical` **birebir aynı olmalıdır**, ayrışırsa Google yinelenen sayfa
uyarısı verir.

`og:type` ders notlarında `article`, hub ve kurumsal sayfalarda `website`.

Paylaşım görseli `og-image.png` (1200×630), `python3 tools/og-gorsel-uret.py`
ile üretilir, elle düzenlenmez. Görseldeki iddialar sitenin kendi metinlerinden
doğrulanabilir olmalı — örneğin "üyelik gerekmez" **yazılamaz**, deneme sınavı
`/panel/` altında ve giriş istiyor.

Panel sayfalarına OG etiketi eklenmez; kapalı içeriğin paylaşım önizlemesi
olmaz.

## H1, yapısal veri ve başlık uzunluğu

**H1.** Her sayfada tam olarak bir H1 bulunur. Ders notlarında bu, `.ders-meta`
içindeki konu adıdır — görsel olarak `.ders-meta b` ile aynı görünmesi için
tarayıcının varsayılan h1 stilleri sıfırlanır. Yani H1 eklemek tasarımı
değiştirmez; zaten başlık gibi görünen öğenin etiketi doğru olur.

**Yapısal veri.** `python3 tools/schema-uret.py` ile üretilir, elle
düzenlenmez; işaretçiler arasındaki blok silinip yeniden yazıldığı için tekrar
tekrar çalıştırılabilir. Veriler sayfanın kendisinden (h1, description,
canonical) okunur, ikinci bir kaynak tutulmaz.

Bilinçli olarak kapsam dışı bırakılanlar script'in başında gerekçesiyle yazılı:
FAQPage (Google 2023'te dar bir otorite grubuna kısıtladı, yanlış işaretleme
manuel eylem riski), SearchAction (site içi arama istemci tarafında, sonuç
URL'i üretmiyor), ders seviyesi kırıntı (`/dersler/ilk-yardim/` diye bir sayfa
yok, 404 döner — ders adı `articleSection` olarak işaretlenir).

**Başlık uzunluğu.** `<title>` 60 karakteri aşmamalı, aşarsa arama sonucunda
ortadan kesilir. Aşan başlıklarda `Konu N:` kısmı atılır — arama değeri yok,
numara sayfada ve yan menüde zaten görünür. `og:title` ve `twitter:title`
`<title>` ile birebir aynı kalmalı.
