# Teknik SEO Denetim Kontrol Listesi

Bulguları önem sırasına göre grupla: **Kritik** (sıralamayı doğrudan engeller) → **Önemli** (sıralamayı zayıflatır) → **İyileştirme** (marjinal kazanç).

## Crawlability & Indexleme (Kritik)
- `robots.txt` sayfayı engelliyor mu?
- `<meta name="robots" content="noindex">` yanlışlıkla eklenmiş mi?
- Sayfa `sitemap.xml` içinde yer alıyor mu?
- Canonical tag (`<link rel="canonical">`) doğru sayfayı işaret ediyor mu, çakışan/döngüsel canonical var mı?
- HTTP durum kodu 200 mü? (301/302 zincirleri, 404, soft-404 kontrol edilmeli)

## Sayfa Hızı & Core Web Vitals (Önemli)
- LCP (Largest Contentful Paint): hedef < 2.5s
- INP (Interaction to Next Paint): hedef < 200ms
- CLS (Cumulative Layout Shift): hedef < 0.1
- Sıkıştırılmamış görseller, render-blocking CSS/JS, önbellekleme eksikliği yaygın nedenlerdir.
- Gerçek ölçüm için PageSpeed Insights / Lighthouse önerilir (bu skill sadece statik sinyalleri kontrol eder).

## Mobil Uyumluluk (Kritik — Google mobile-first indexler)
- Viewport meta etiketi var mı? (`<meta name="viewport" content="width=device-width, initial-scale=1">`)
- Metin/dokunma hedefleri mobilde okunabilir/tıklanabilir mi?
- Yatay kaydırma gerektiren taşan içerik var mı?

## Yapısal Veri (Structured Data)
- Sayfa türüne uygun schema.org işaretlemesi var mı? (Article, Product, FAQ, BreadcrumbList vb.)
- JSON-LD formatı tercih edilir, sözdizimi hatasız olmalı (Google Rich Results Test ile doğrulanabilir).

## HTTPS & Güvenlik
- Site HTTPS üzerinden mi sunuluyor?
- Karışık içerik (mixed content) uyarısı var mı?

## Site Mimarisi
- Önemli sayfalar ana sayfadan kaç tıklamada erişilebiliyor? (3 tıklama kuralı)
- Yetim sayfalar (hiçbir yerden linklenmeyen) var mı?
- Facet/parametre URL'leri gereksiz index şişmesine yol açıyor mu?

## Uluslararasılaştırma (varsa)
- `hreflang` etiketleri doğru ve karşılıklı (reciprocal) mi?

## Script Kullanımı
`scripts/audit_page.py` bir URL'nin HTML'ini indirip şu sinyalleri statik olarak çıkarır: title/meta açıklama uzunluğu, H1 sayısı ve içeriği, alt metni eksik görseller, canonical, robots meta, temel structured data varlığı, kelime sayısı. JavaScript ile sonradan render edilen (client-side rendered) sayfalarda script eksik/yanlış sonuç verebilir — bu durumu kullanıcıya belirt.
