// Firebase başlatma — tüm sayfalar bu modülü kullanır.
//
// Buradaki değerler GİZLİ DEĞİLDİR; istemcide zaten görünürler ve Google'ın
// dokümantasyonu da repoda tutulmalarını normal karşılar. Erişimi koruyan şey
// bu anahtarlar değil, Firestore güvenlik kuralları ve sunucu tarafındaki
// yetki kontrolüdür.

import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import {
  getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged
} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
// Firestore BİLEREK statik import edilmiyor — panel-kabuk.js'teki gerekçenin
// aynısı. Bu SDK 117 KB ve yalnızca profil ile deneme işlemlerinde gerekiyor;
// bu işlemlerin hepsi kullanıcı giriş yaptıktan sonra çalışıyor. Statikken her
// genel sayfa (43 ders notu dahil) açılışta bu 117 KB'ı boşuna indiriyordu.
//
// Auth statik kalıyor: başlıktaki giriş durumu sayfa açılır açılmaz doğru
// çizilmeli, onu geciktirmek görünür bir titremeye yol açar.

const firebaseConfig = {
  apiKey: 'AIzaSyDmyoZ-Wa-zqzimqaIV--9tN2TFdvhRcmo',
  // Google giriş ekranında bu adres görünür. Kendi alan adımızı kullanmak
  // ÜÇ parçanın birlikte durmasına bağlı; biri eksikse giriş tamamen kırılır
  // (Error 400: redirect_uri_mismatch):
  //   1. buradaki authDomain
  //   2. vercel.json içindeki /__/auth/* yönlendirmesi
  //   3. Google Cloud OAuth istemcisinde kayıtlı olması gerekenler:
  //      - Authorized JavaScript origins:  https://ehliyet.digital
  //      - Authorized redirect URIs:       https://ehliyet.digital/__/auth/handler
  // Bunlardan birini değiştirmeden önce diğer ikisini doğrula.
  authDomain: 'ehliyet.digital',
  projectId: 'ehliyet-52d4d',
  storageBucket: 'ehliyet-52d4d.firebasestorage.app',
  messagingSenderId: '40944921621',
  appId: '1:40944921621:web:66cc2e67bb8cb45464f21c',
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

/*
 * Firestore'u ilk ihtiyaç anında indirir ve önbelleğe alır; sonraki çağrılar
 * aynı promise'i döner, SDK bir kez iner.
 *
 * `db` artık dışarı verilmiyor: modülün dışında kimse kullanmıyordu ve dışarı
 * verilse eş zamanlı okunamazdı — SDK henüz inmemiş olabilir. Firestore'a
 * ihtiyaç duyan her fonksiyon aşağıda `await fs()` ile başlıyor.
 */
let _fs;
function fs() {
  _fs ??= import('https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js')
    .then(m => ({ ...m, db: m.getFirestore(app) }));
  return _fs;
}

const provider = new GoogleAuthProvider();
provider.setCustomParameters({ prompt: 'select_account' });

/*
 * Google girişi küçük bir açılır PENCEREDE yapılır; arkada ürün görünür kalır.
 * Yönlendirme (signInWithRedirect) bilerek kullanılmıyor: sayfayı tamamen
 * Google ekranına çeviriyor ve kullanıcı ürünle bağını kaybediyor.
 *
 * DİKKAT — bu fonksiyon kullanıcının tıklamasıyla ARADA await olmadan
 * çağrılmalı. Araya bir bekleme girerse Chrome pencereyi tıklamaya bağlı
 * saymıyor ve küçük pencere yerine yeni sekme açıyor (ya da hiç açmıyor).
 * Çağıran taraf oturum durumunu önceden çözmüş olmalı.
 */
export function girisYap() {
  return signInWithPopup(auth, provider);
}

export function cikisYap() {
  return signOut(auth);
}

/*
 * Oturum ipucu.
 *
 * Firebase'in oturum durumunu çözmesi SDK'nın CDN'den inmesini gerektiriyor;
 * bu süre boyunca sayfa "Yükleniyor…" göstermek zorunda kalıyordu. Daha önce
 * giriş yapıldığını yerelde işaretleyip, kabuğu Firebase'i beklemeden kurmak
 * için kullanıyoruz.
 *
 * Bu bir yetkilendirme aracı DEĞİLDİR — kullanıcı bu değeri kendi elleriyle
 * yazabilir. Yalnızca "muhtemelen giriş yapmış, ekranı şimdiden çizebiliriz"
 * anlamına gelir. Gerçek karar her zaman onAuthStateChanged'den gelir ve
 * oturum yoksa yönlendirme yine yapılır.
 */
const OTURUM_IPUCU = 'ehliyet-oturum';

export function oturumBekleniyorMu() {
  try {
    return localStorage.getItem(OTURUM_IPUCU) === '1';
  } catch {
    return false;
  }
}

export function kullaniciDinle(cb) {
  return onAuthStateChanged(auth, (user) => {
    try {
      if (user) localStorage.setItem(OTURUM_IPUCU, '1');
      else localStorage.removeItem(OTURUM_IPUCU);
    } catch { /* localStorage kapalıysa ipucu olmadan devam ederiz */ }
    cb(user);
  });
}

/** Google'dan gelen tek parça adı ad ve soyad olarak ayırır. */
function adiAyir(tamAd) {
  const parcalar = String(tamAd || '').trim().split(/\s+/).filter(Boolean);
  if (!parcalar.length) return { ad: '', soyad: '' };
  // Son kelime soyad, kalanı ad — çok adlı isimlerde doğru sonuç verir.
  return { ad: parcalar.slice(0, -1).join(' ') || parcalar[0], soyad: parcalar.length > 1 ? parcalar.at(-1) : '' };
}

/** Giriş sonrası profil dokümanını oluşturur ya da son giriş zamanını günceller. */
export async function profiliHazirla(user) {
  const { db, doc, getDoc, setDoc, serverTimestamp } = await fs();
  const ref = doc(db, 'users', user.uid);
  const mevcut = await getDoc(ref);

  if (!mevcut.exists()) {
    // Alanlar güvenlik kurallarındaki beyaz listeyle birebir aynı olmalı.
    const { ad, soyad } = adiAyir(user.displayName);
    await setDoc(ref, {
      email: user.email,
      ad,
      soyad,
      telefon: '',
      ehliyetTuru: '',
      fotoUrl: user.photoURL || '',
      olusturulmaAt: serverTimestamp(),
      sonGirisAt: serverTimestamp(),
    });
  } else {
    await setDoc(ref, { sonGirisAt: serverTimestamp() }, { merge: true });
  }
  return ref;
}

/** Profil verisini okur; doküman yoksa null döner. */
export async function profiliGetir(uid) {
  const { db, doc, getDoc } = await fs();
  const snap = await getDoc(doc(db, 'users', uid));
  return snap.exists() ? snap.data() : null;
}

/**
 * Profilin düzenlenebilir alanlarını kaydeder.
 * E-posta bilerek dışarıda: kullanıcının kimliği Google hesabıdır ve
 * güvenlik kuralları da güncellemede e-posta yazılmasına izin vermez.
 */
export async function profiliKaydet(uid, { ad, soyad, telefon, ehliyetTuru }) {
  const { db, doc, setDoc } = await fs();
  return setDoc(doc(db, 'users', uid), {
    ad: ad ?? '',
    soyad: soyad ?? '',
    telefon: telefon ?? '',
    ehliyetTuru: ehliyetTuru ?? '',
  }, { merge: true });
}

/** Bitmiş bir sınav denemesini kaydeder. */
export async function denemeKaydet(uid, sonuc) {
  const { db, addDoc, collection, serverTimestamp } = await fs();
  return addDoc(collection(db, 'users', uid, 'denemeler'), {
    ...sonuc,
    kaydedilmeAt: serverTimestamp(),
  });
}

/**
 * Geri bildirimi `feedback` koleksiyonuna kaydeder. Giriş şart değildir:
 * public sitedeki ziyaretçi de gönderebilir, o durumda uid null yazılır.
 * Koleksiyon istemciden okunamaz (güvenlik kuralları); kayıtlar Firebase
 * konsolundan ya da Admin SDK ile okunur.
 */
export async function geriBildirimKaydet({ mesaj, email, puan }) {
  const { db, addDoc, collection, serverTimestamp } = await fs();
  return addDoc(collection(db, 'feedback'), {
    mesaj: String(mesaj).slice(0, 2000),
    // Girişli kullanıcıda form e-posta sormaz; adres hesabından alınır.
    email: String(email || auth.currentUser?.email || '').slice(0, 200),
    // Puan isteğe bağlı: 1-5 arası tam sayı, verilmediyse null.
    puan: Number.isInteger(puan) && puan >= 1 && puan <= 5 ? puan : null,
    sayfa: location.pathname,
    uid: auth.currentUser?.uid ?? null,
    olusturulmaAt: serverTimestamp(),
  });
}

/** Kullanıcının geçmiş denemelerini yeniden eskiye döner. @param {number} [sinir] opsiyonel limit */
export async function denemeleriGetir(uid, sinir) {
  const { db, collection, query, orderBy, getDocs, limit } = await fs();
  const kisitlar = [orderBy('kaydedilmeAt', 'desc')];
  if (sinir) kisitlar.push(limit(sinir));
  const q = query(collection(db, 'users', uid, 'denemeler'), ...kisitlar);
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}

/** Kullanıcı hesabını ve tüm Firestore verisini siler. */
export async function hesabiSil(user) {
  const { db, doc, deleteDoc, collection, getDocs } = await fs();

  // Alt koleksiyonları sil (denemeler, yetkiler vb.)
  const altKollar = ['denemeler', 'yetkiler'];
  for (const kol of altKollar) {
    try {
      const snap = await getDocs(collection(db, 'users', user.uid, kol));
      for (const d of snap.docs) await deleteDoc(d.ref);
    } catch (_) { /* koleksiyon yoksa sorun değil */ }
  }

  // Ana profil dokümanını sil
  await deleteDoc(doc(db, 'users', user.uid));

  // Firebase Auth hesabını sil
  const { deleteUser } = await import('https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js');
  await deleteUser(user);
}
