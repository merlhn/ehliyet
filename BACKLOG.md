# Backlog

Açık işler ve bekleyen kararlar. Tamamlananlar en alta taşınır.

---

## Sıradaki

### 1. Google giriş ekranında kendi domainimiz görünsün
Şu an onay ekranında `ehliyet-52d4d.firebaseapp.com` yazıyor, güven kırıyor.

- `assets/js/firebase.js` → `authDomain: 'ehliyet.digital'`
- `vercel.json` içindeki `/__/auth/*` rewrite'ı zaten hazır

**İkisi birlikte değiştirilmeli.** Tek başına `authDomain`'i değiştirmek girişi tamamen kırar.
`/__/auth/handler` canlıda test edildi, proxy çalışıyor — değişiklik yapılabilir durumda.

### 2. OAuth onay ekranı kimliği
Google Cloud Console → APIs & Services → OAuth consent screen → Branding

- App name: `ehliyet.digital`
- App logo (onay ekranında görünür, dönüşümü belirgin etkiler)
- Application home page: `https://ehliyet.digital`
- Privacy policy: `https://ehliyet.digital/gizlilik/`
- Terms of service: `https://ehliyet.digital/kullanim-sartlari/`

Son ikisi Google'ın doğrulama sürecinde de isteniyor.

### 3. Gizlilik metnini KVKK'ya göre güncelle
Artık kişisel veri işliyoruz; mevcut metin bunu kapsamıyor.

- Google hesabından alınan veriler: ad, e-posta, profil fotoğrafı
- Saklanan veriler: sınav sonuçları, sınav yetkileri
- Verinin nerede tutulduğu (Firebase / Google Cloud, `eur3` Avrupa)
- Silme talebi nasıl yapılır

### 4. Panelde profil ekranı
`/panel/` içinde profil şu an "yakında geliştirilecek" yer tutucusu. Eski `/profil/`
sayfası silindi, yeniden tasarlanacak. Sınav geçmişi tablosu da buraya taşınacak.

### 5. Panelde Settings ekranı
Yer tutucu durumda. İçeriği belirlenmedi.

### 6. Sınav sonucunu kaydet
Sınav bitince `users/{uid}/denemeler` altına yaz. Okuma tarafı (`denemeleriGetir`)
hazır, panelde gösterilecek yer profil ekranı olacak.

### 7. Logo entegrasyonu
`assets/img/marka/logo.png` panelde kullanılıyor. Eksikler:
- Favicon seti — logo ince çizgili ve detaylı, 16-32px'te okunmuyor; sadeleştirilmiş
  varyant gerekiyor
- Public site header'ında marka görünmüyor, sadece nav var
- OAuth onay ekranı için kare logo yüklenmesi

### 8. Sınav sayfalarına giriş zorunluluğu
`deneme-sinavlari/sinav-N/` ve kılavuz sayfalarına `auth-ui` bilerek eklenmedi
(header'ları farklı: sayaç, "Sınavı Bitir"). Giriş yapmamış kullanıcı sınava
başlayamamalı.

### 9. Ücretli içeriğin korunması — **kritik**
Şu an soru bankaları herkese açık: `https://ehliyet.digital/assets/js/questions-2.js`
adresini açan 50 soruyu cevaplarıyla görür. Ödeme eklenmeden önce mutlaka çözülmeli,
yoksa satılan şey zaten bedava indirilebilir durumda.

- Ücretli soru bankaları public klasörden çıkarılır (içerik yine git'te kalır)
- `/api/sorular?sinav=N` → Firebase ID token doğrula → yetki kontrol et → JSON dön
- Sınav sayfası soruları `<script src>` yerine bu uçtan çeker
- Repoya `package.json` ve `api/` girer; proje tam statik olmaktan çıkar

1. fazda kural "hesabı var mı?", ödeme gelince "bu sınava yetkisi var mı?" olur —
mimari değişmez.

---

## Sonraki faz

### Ödeme
Sınav 1 ücretsiz, diğerleri ücretli. Yetki kayıtları (`users/{uid}/yetkiler/{sinavId}`)
yalnızca sunucu tarafında yazılır; istemcinin yazması Firestore kurallarıyla engelli.
Sağlayıcı seçilmedi.

### Sınav 3 ve sonrası
Akış `README.md` içinde. `../Sınav_N/` klasöründen `assets/js/questions-N.js` +
`deneme-sinavlari/sinav-N/` üretilir. Cevaplar yayına alınmadan önce anahtarla
programatik doğrulanmalı.

---

## Bilinen kabuller

**Sınav puanı istemcide hesaplanıyor.** Teknik bilgisi olan biri sahte sonuç yazabilir.
Veri kişisel ilerleme takibi olduğu için şimdilik kabul edilebilir. Sıralama, rozet
veya sertifika gibi rekabetçi bir özellik eklenirse puanlama sunucuya taşınmalı.

**Gizli sayfa ≠ erişim kontrolü.** `noindex` ve link vermemek sayfayı aramadan ve
gezinmeden çıkarır, ama linke sahip olan herkes açar.

---

## Tamamlananlar

- Sınav 2 eklendi (50 soru, cevap anahtarıyla doğrulandı, 38 medya dosyası)
- Klasör yapısı yeniden düzenlendi: `/dersler/` ve `/deneme-sinavlari/` kardeş bölümler,
  varlıklar `/assets/` altında, URL'ler kebab-case ve ASCII
- Proje `ehliyet.digital` olarak adlandırıldı, Vercel'e deploy edildi
- Firebase kuruldu: Google girişi, Firestore (`eur3`), güvenlik kuralları
- Header'a Google ile giriş butonu ve profil menüsü
- `ehliyet.digital` alan adı bağlandı; www kalıcı olarak apex'e yönleniyor
- Header düzeni içerik kutusuyla hizalandı, mobil sıkışma giderildi
- Giriş sonrası panel (`/panel/`): yan menü, üst bar, deneme sınavları listesi

---

## İptal edilenler

- **Deneme sınavlarının PDF olarak indirilmesi.** Video içeren sorular kağıda
  aktarılamadığı için gizli bir video alanı (`/v/<sinav>/<soru>/`) kurulmuştu;
  PDF işi iptal edilince o sayfalar da silindi.
