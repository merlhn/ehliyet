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
import {
  getFirestore, doc, getDoc, setDoc, addDoc, collection,
  query, orderBy, getDocs, serverTimestamp
} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js';

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
export const db = getFirestore(app);

const provider = new GoogleAuthProvider();
provider.setCustomParameters({ prompt: 'select_account' });

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

/** Giriş sonrası profil dokümanını oluşturur ya da son giriş zamanını günceller. */
export async function profiliHazirla(user) {
  const ref = doc(db, 'users', user.uid);
  const mevcut = await getDoc(ref);

  if (!mevcut.exists()) {
    // Alanlar güvenlik kurallarındaki beyaz listeyle birebir aynı olmalı.
    await setDoc(ref, {
      email: user.email,
      ad: user.displayName || '',
      fotoUrl: user.photoURL || '',
      olusturulmaAt: serverTimestamp(),
      sonGirisAt: serverTimestamp(),
    });
  } else {
    await setDoc(ref, { sonGirisAt: serverTimestamp() }, { merge: true });
  }
  return ref;
}

/** Bitmiş bir sınav denemesini kaydeder. */
export async function denemeKaydet(uid, sonuc) {
  return addDoc(collection(db, 'users', uid, 'denemeler'), {
    ...sonuc,
    kaydedilmeAt: serverTimestamp(),
  });
}

/** Kullanıcının geçmiş denemelerini yeniden eskiye döner. */
export async function denemeleriGetir(uid) {
  const q = query(collection(db, 'users', uid, 'denemeler'), orderBy('kaydedilmeAt', 'desc'));
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}
