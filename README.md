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
