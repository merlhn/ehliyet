# -*- coding: utf-8 -*-
# Hap Bilgiler sayfalarını üretir ve 6 public sayfanın footer'ını sütunlu yapıya çevirir.
# Tek seferlik üretim scripti; içerik questions-1.js + questions-2.js analizinden.
import os, sys, re, unicodedata

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------- hap slug ----
# Her hap bilginin kendi sayfası var: /hap-bilgiler/{kategori}/{slug}/
# Slug burada üretilir; tools/hap-sayfa-uret.py da aynı fonksiyonu kullanır,
# böylece kategori sayfasındaki link ile üretilen sayfa yolu ayrışamaz.

_TR_MAP = str.maketrans({
    "ş": "s", "Ş": "s", "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g",
    "ı": "i", "İ": "i", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u",
})

def duz_metin(html_metin):
    """Hap bilgideki <b> gibi etiketleri atar."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html_metin)).strip()

def slugify(text, max_len=60):
    """Türkçe uyumlu kebab-case slug (soru-sayfa-uret.py ile aynı kural)."""
    s = text.translate(_TR_MAP).lower()
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s.strip())
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    if len(s) > max_len:
        s = s[:max_len]
        last_dash = s.rfind("-")
        if last_dash > max_len // 2:
            s = s[:last_dash]
    return s

def hap_listesi(d):
    """Bir dersin hap bilgilerini sırayla döndürür: (sira, grup, html, duz, slug).
    Slug çakışmalarında -2, -3 eki eklenir (deterministik)."""
    sonuc, kullanilan, sira = [], set(), 0
    for grup_ad, bilgiler in d["gruplar"]:
        for b in bilgiler:
            sira += 1
            duz = duz_metin(b)
            slug = taban = slugify(duz) or f"hap-{sira:02d}"
            n = 2
            while slug in kullanilan:
                slug = f"{taban}-{n}"; n += 1
            kullanilan.add(slug)
            sonuc.append((sira, grup_ad, b, duz, slug))
    return sonuc

# ---------------------------------------------------------------- içerik ----

DERSLER = [
  {
    "slug": "ilk-yardim",
    "ad": "İlk Yardım",
    "ders_link": "/dersler/ilk-yardim/ilk-yardim-ve-acil-tedavi/",
    "kart": "Temel yaşam desteği, kanamalar, kırıklar, pozisyonlar ve taşıma teknikleri.",
    "ozet": "Deneme sınavlarındaki İlk Yardım sorularını çözdüren bilgiler: sayılar, sıralamalar ve müdahale kuralları.",
    # Landing kartında gösterilen örnekler: gruplardaki bilgilerin kısaltılmış hâli.
    # Hero'daki HERO_ORNEKLER ile çakışmasın diye farklı bilgiler seçildi.
    "on_izleme": [
      "Fışkırır tarzda kanama, atardamar kanamasıdır.",
      "Köprücük kemiği kırığı, çapraz (sekiz) bandajla tespit edilir.",
    ],
    "ikon": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "gruplar": [
      ("Temel yaşam desteği", [
        'Hayat kurtarma zincirinin sırası: <b>112’ye haber verilir → olay yerinde temel yaşam desteği yapılır → ambulans ekipleri müdahale eder → hastane acil servisinde tedavi edilir</b>.',
        'Yetişkinde temel yaşam desteği <b>30 kalp masajı + 2 yapay solunum</b> döngüsüyle uygulanır ve uygulamaya <b>kalp masajıyla başlanır</b>.',
        'Yetişkinde kalp masajı: göğüs kemiği <b>5–6 cm</b> çökecek şekilde, dakikada <b>100–120</b> bası. (3 cm ya da dakikada 30 bası yanlıştır.)',
        'Bebekte kalp basısı, bir elin <b>orta ve yüzük parmağıyla</b>, iki meme başını birleştiren hattın <b>hemen altına</b> yapılır.',
        'Hava yolunu açan pozisyon <b>baş geri–çene yukarı</b>: bir el alna, diğer elin iki parmağı çene kemiğine konur; alından bastırılıp çeneden kaldırılır.',
        'Kazazedenin <b>ağzı ve çevresinde yaralanma</b> varsa yapay solunum <b>ağızdan buruna</b> yapılır.',
        'Solunum yolu tam tıkanan bebekte: önce yüzüstü pozisyonda <b>5 sırt darbesi</b>, ardından sırtüstü çevrilip <b>5 göğüs basısı</b> uygulanır.',
      ]),
      ("Bilinç bozuklukları ve pozisyonlar", [
        'Bayılma, <b>kısa süreli, yüzeysel ve geçici bilinç kaybı</b>dır.',
        'Bilinci kapalı ama <b>solunumu ve nabzı olan</b> kazazedeye <b>koma (yarı yüzükoyun-yan yatış)</b> pozisyonu verilir. Baş-omurga yaralanması yoksa hava yolu açıklığı bu pozisyonla korunur.',
        'Bayılan kazazedede sıkan giysiler <b>gevşetilir</b> ve solunum yolu açıklığı korunur. Ayakları 45 cm kaldırmak ya da yarı oturtmak bayılmada <b>uygulanmaz</b>.',
        'Şokun belirtileri: deri <b>soluk, soğuk ve nemli</b>, gözler donuk, bilinç bulanık. Kazazedenin üzeri örtülerek <b>vücut sıcaklığı korunur</b>; ağızdan içecek verilmez.',
        'Kalp krizinin tipik ağrısı <b>dinlenmekle geçmez</b>; kravat bölgesinde hissedilir, <b>omuzlara, boyuna, çeneye ve sol kola</b> yayılır, ölüm korkusu eşlik eder.',
        '<b>Omurilik</b>, omurga kanalı içinde boyundan kuyruk sokumuna uzanır; beyin ile vücut arasındaki bağlantıyı sağlar ve <b>reflekslerin merkezi</b>dir.',
      ]),
      ("Kanamalar ve yaralanmalar", [
        'Fışkırır tarzda kanama <b>atardamar</b> kanamasıdır: bölge yukarı kaldırılır, temiz bezle baskı yapılır, bez kaldırılmadan üzerinden bandajla sarılır. Elle baskı, kanayan yere <b>en yakın</b> basınç noktasına uygulanır — en uzak noktaya değil.',
        'Kulaktan kanama ve göz çevresinde morluk, <b>kafatası yaralanması</b> işaretidir: kazazede <b>yarı oturur pozisyona alınmaz</b>; boyun tespiti yapılır, yaşam bulguları (ABC) değerlendirilir.',
      ]),
      ("Kırıklar", [
        '<b>Açık kırıkta deri bütünlüğü bozulur</b>; kan kaybı ve enfeksiyon riski yüksektir. Deri bütünlüğünün korunduğu kırık, kapalı kırıktır.',
        '<b>Köprücük kemiği</b> kırığında tespit, her iki omuz üzerinden geçen <b>çapraz (sekiz) bandajla</b> yapılır.',
        'Kalça ve alt taraf kırıklarının tespitinde: açık kırık varsa yara önce <b>temiz bir bezle kapatılır</b>; destek malzemeleri yumuşak olmalı, sargı kırığın üzerine bağlanmamalı, yaralı oturtulmamalıdır.',
      ]),
      ("Taşıma teknikleri", [
        'Taşımada genel kural: <b>baş-boyun-gövde ekseni</b> bozulmadan, kazazede <b>en az 6 destek noktasından</b> kavranır ve mümkün olduğunca az hareket ettirilir. Kaldırırken ağırlık karın değil <b>bacak kaslarına</b> verilir.',
        '<b>Rentek manevrası</b>: solunumu durmuş ya da tehlike altındaki kazazedeyi, ayakları pedala sıkışmamışsa araç içinden çıkarma tekniğidir.',
        '<b>Teskereci yöntemi</b>, kaşık ve köprü teknikleri kazazedeyi sedyeye yerleştirmek için kullanılır.',
      ]),
    ],
  },
  {
    "slug": "trafik-ve-cevre",
    "ad": "Trafik ve Çevre",
    "ders_link": "/dersler/trafik-ve-cevre/temel-tanimlar/",
    "kart": "İşaretler, şerit ve geçme kuralları, duraklama mesafeleri, geçiş üstünlüğü ve cezalar.",
    "ozet": "Deneme sınavlarındaki Trafik ve Çevre sorularını çözdüren bilgiler: mesafeler, süreler, sıralamalar ve kurallar.",
    "on_izleme": [
      "Yangın musluklarına 5 metre mesafede duraklamak yasaktır.",
      "100 ceza puanını ilk kez aşan sürücünün belgesi 2 ay geri alınır.",
    ],
    "ikon": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "gruplar": [
      ("Kurumlar ve yetkiler", [
        'Kara yollarında hız sınırlarını (yönetmeliktekinin üstünde ya da altında) belirlemek ve işaretlemek, İçişleri Bakanlığının uygun görüşüyle <b>Karayolları Genel Müdürlüğünün</b> yetkisidir.',
        'Şehir içinde yol yapısı ya da işaretleme yetersizliği yüzünden kaza olan yerlerde teklif edilen tedbirleri almak <b>belediyenin</b> görevidir.',
      ]),
      ("Işıklar ve levhalar", [
        '<b>Aralıklı yanıp sönen kırmızı ışık, DUR levhasıyla</b> aynı anlamdadır: durulur, yol uygunsa devam edilir.',
        'Gişe simgeli otoyol bilgi levhası, <b>ücretli otoyola</b> girileceğini bildirir.',
        '“Şerit azalması” levhası görülünce yapılacak şey: <b>yavaşlayıp devam eden (sağ) şeride girmek</b> — hızlanıp şeritte ısrar etmek değil.',
      ]),
      ("Şerit ve geçme kuralları", [
        'Geçme ve dönme gibi <b>mecburi hâller dışında şerit değiştirmek</b> kural ihlalidir. Şerit değiştirmeden önce girilecek şeritteki araçların güvenle geçişi beklenir.',
        'İki yönlü üç şeritli yolda <b>orta şerit yalnızca geçme (sollama)</b> içindir; orta şeridi sürekli işgal etmek hatalı sollamadır.',
        'Önündeki araç geçiş hâlindeyken karşıdan araç geliyorsa sürücü <b>öndeki aracın geçişini bekler</b>; sol şeride çıkmaz.',
        'Arkadan çarpma şeklindeki kazaların en önemli sebebi <b>takip mesafesi kuralına uyulmamasıdır</b>.',
      ]),
      ("Hız, mesafe ve farlar", [
        'Durma mesafesini etkileyen etkenler: aracın hızı, yolun eğimi ve kaplamanın cinsi. <b>Hidrolik direksiyon durma mesafesini etkilemez.</b>',
        'Ortalama hız tespiti yapılan yol kesiminde levhadaki sınır, iki nokta arasındaki <b>ortalama hız</b> için geçerlidir; araçlar en fazla bu hızla ilerleyebilir.',
        'Uzun hüzmeli fardan kısa fara geçilir: <b>yeterince aydınlatılmış yola girince</b> ve <b>geceleyin öndeki aracı geçerken</b>.',
        'Gece kısa farla net görüş mesafesi ortalama <b>25 metredir</b>; hız, tehlike anında bu mesafe içinde <b>durulabilecek</b> seviyeye indirilir.',
      ]),
      ("Duraklama ve park", [
        'Duraklamak yasaktır: trafik işaretiyle yasaklanmış yerlerde, <b>yangın musluklarına 5 metre</b> ve yerleşim yeri içinde <b>kavşak ve bağlantı yollarına 5 metre</b> mesafede.',
        'İşaret levhalarına yaklaşım yönünde duraklama yasağı: yerleşim birimi <b>içinde 15 metre</b>, <b>dışında 100 metre</b>.',
        'Duraklanan ya da park edilen yerden çıkarken: çıkış işareti verilir, araç ve etrafı kontrol edilir, görüş dışı noktalar varsa <b>gözcü bulundurulur</b>. Yoldan geçen araçları durdurmak kurala aykırıdır.',
      ]),
      ("Geçiş üstünlüğü ve öncelik", [
        'Geçiş üstünlüğü sıralaması: <b>ambulans ve yaralı taşıyan araçlar → organ-doku nakli araçları → itfaiye ve acil müdahale araçları → güvenlik güçleri</b>.',
        'Geçiş üstünlüğü olan aracın sireni duyulduğunda ilk yapılacak şey <b>sesin yönünü tayin etmektir</b>.',
        'Dar köprü gibi kesimlerde karşılaşan araçlardan geçiş önceliği <b>karşıdaki araca bırakılır</b>; hızlanıp köprüye önce girmeye çalışmak yanlıştır.',
      ]),
      ("Belge ve cezalar", [
        'Bir yıl içinde <b>100 ceza puanını ilk kez aşan</b> sürücünün belgesi <b>2 ay</b> geri alınır.',
        '<b>Ölümle sonuçlanan kazada asli kusurlu</b> sürücünün belgesi mahkemece <b>1 yıl</b> geri alınır.',
      ]),
      ("Araç, yük ve muayene", [
        'Kamyon, kamyonet ve römorkta yükle birlikte yolcu taşınırken: kasanın yan ve arka kapakları <b>kapalı</b>, yük <b>sağlam yerleştirilmiş ve bağlanmış</b> olmalıdır.',
        'Emniyet kemeri zorunluluğunun amacı, kaza anında <b>ölüm ve yaralanmaları en aza indirmektir</b>.',
        'Araç muayenesinde <b>ağır kusur</b> sayılır: rot başlarının boşluk yapması, ön cam sileceklerinin çalışmaması, park lambalarının yanmaması.',
        'Kaza oranını etkileyen etmenler: kural ihlalleri, araç bakımları ve aracın yük durumu. <b>Aracın beygir gücü etkilemez.</b>',
      ]),
      ("Çevre", [
        'Atıkların <b>toplanıp işlenerek yeniden kullanılması</b> çevreye zarar değil, faydadır; koku, çirkin görünüm ve hastalık taşıyıcıların üremesi ise zararlarıdır.',
        'Araç bakımlarını ve egzoz emisyon ölçümünü <b>zamanında yaptırmak</b> çevrenin temiz kalmasına katkı sağlar.',
      ]),
    ],
  },
  {
    "slug": "arac-teknigi",
    "ad": "Araç Tekniği",
    "ders_link": "/dersler/arac-teknigi/motor-nedir/",
    "kart": "Gösterge paneli ikazları, motor sistemleri, bakım kuralları ve ekonomik sürüş.",
    "ozet": "Deneme sınavlarındaki Araç Tekniği sorularını çözdüren bilgiler: ikaz ışıkları, arıza sebepleri ve bakım kuralları.",
    "on_izleme": [
      "ABS uyarı ışığı, fren sisteminde arıza olduğunu bildirir.",
      "Motorun hararet yapma sebeplerinden biri termostat arızasıdır.",
    ],
    "ikon": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "gruplar": [
      ("Gösterge paneli ikazları", [
        '<b>ABS uyarı ışığı</b>, <b>fren sisteminde</b> arıza olduğunu bildirir.',
        'Motor yağlama yapmadığında <b>kırmızı yağdanlık (yağ) lambası</b> yanar.',
        '<b>Şarj</b> ve <b>yağ basıncı</b> lambaları yanarsa araç kurallara uygun şekilde <b>derhal durdurulur ve kontak kapatılır</b>. ABS ışığı bu grupta değildir.',
        'Lastik basıncı (TPMS) ikazı; basınç azaldığında, lastik patladığında ve sensör arızalandığında yanar — <b>lastik ısındığında yanmaz</b>.',
        'Cam yıkama suyu ikazı yandığında <b>silecek suyu deposuna su eklenir</b>.',
      ]),
      ("Motor ve sistemler", [
        'Motor soğutma sisteminin elemanları: <b>radyatör, su pompası ve termostat</b>. Balata fren sistemi elemanıdır.',
        'Motorun <b>hararet</b> yapma sebepleri: termostat arızası, devirdaim (su) hortumunun yırtılması, vantilatör kayışının gevşemesi. Antifriz seviyesinin düşük olması hararet sebebi sayılmaz.',
        '<b>Silindir kapak contası</b> işlevini kaybederse motorun içine <b>su sızar</b>.',
        '<b>V kayışı</b> düzgün çalışmazsa <b>şarj ikaz lambası</b> yanar.',
        'Motor yağı kontrol sırası: <b>düz zeminde dur, kaputu aç → çubuğu çekip temizle → tekrar daldırıp çek → seviyenin max–min arasında olduğunu gör</b>.',
        'Dizel araca yanlışlıkla benzin konursa <b>yakıt deposu boşaltılır</b>; araç bu yakıtla kullanılmaz.',
      ]),
      ("Bakım ve kullanım", [
        'Muayene süresi dolmasa bile aracın <b>özel teknik muayenesi, trafik zabıtasının gerekli görmesi</b> hâlinde zorunludur.',
        'Araç çok uzun süre kullanılmazsa <b>akü şarjı azalır</b> ve <b>motor yağı özelliğini kaybeder</b>. Fren balataları kullanılmayan araçta azalmaz.',
        '<b>Antifriz yoğunluğu ölçümü</b> servis ya da tamir atölyesinin işidir; silecek, lastik basıncı ve yağ seviyesi kontrolünü sürücü kendisi yapar.',
        'Sürüşe başlamadan önce <b>koltuk ve ayna ayarı</b>, sürüş konforu ve <b>güvenliği</b> için yapılır.',
        'Yakıt tüketimini azaltır: ani duruş-kalkıştan kaçınmak, tavsiye edilen lastikleri kullanmak, bakımları zamanında yaptırmak. Artırır: <b>vitese göre yanlış devirde sürmek</b> ve ilk çalıştırmada motora tam güç vermek.',
        'Egzozdan çıkan yoğun duman, <b>motorun düzensiz çalıştığının</b> işaretidir.',
      ]),
    ],
  },
  {
    "slug": "trafik-adabi",
    "ad": "Trafik Adabı",
    "ders_link": "/dersler/trafik-adabi/temel-kavramlar/",
    "kart": "Trafikteki değerler, hak ihlalleri, stres yönetimi ve iletişim kuralları.",
    "ozet": "Deneme sınavlarındaki Trafik Adabı sorularını çözdüren bilgiler: değer kavramları, davranış örnekleri ve hak ihlalleri.",
    "on_izleme": [
      "Feragat, kendi hakkından başkası yararına vazgeçebilmektir.",
      "Trafikte yaşanan stres kaygıyı artırır, kalp atışını hızlandırır.",
    ],
    "ikon": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "gruplar": [
      ("Değerler", [
        '<b>Diğerkâmlık</b>: başkasını da düşünmek — kendini geçmekte olan araca yavaşlayarak kolaylık sağlamak bu değerin örneğidir.',
        '<b>Feragat</b>: kendi hakkından başkası yararına vazgeçebilmektir.',
        'Yardım araçlarına kolaylık sağlayan sürücü <b>feragate, diğerkâmlığa ve empatiye</b> önem verir — <b>aceleciliğe değil</b>.',
        'Toplum adabına aykırı davranış: kaza, deprem, sel gibi felaketlerden <b>çıkar sağlamaya çalışmak</b>.',
      ]),
      ("Davranışlar", [
        'Trafik adabına sahip sürücü, kuralların <b>nedenini öğrenir</b> ve ihlalin kendisinin ya da sevdiklerinin <b>canını tehlikeye attığının</b> farkındadır. İhlali yalnızca “maddi ceza” sanmak adaba aykırıdır.',
        '<b>Sürekli ve ani şerit değiştirerek</b> araç kullanmak, diğer sürücülerin dikkatinin dağılmasına ve paniğe kapılmalarına sebep olur.',
        'Engellilere ayrılmış alana ya da hissedilebilir yüzeyin üzerine park eden sürücünün <b>sorumluluk bilinci zayıftır</b>.',
        'Karşıya geçen yayayı el, kol ve sözle acele ettiren sürücü <b>sabırlı davranamamıştır</b>.',
      ]),
      ("İletişim, stres ve hak ihlalleri", [
        'Başarılı iletişim için sürücü <b>insanların değişebileceğine inanmalıdır</b>; dinlerken yargılamak, iletişime kapanmak ve tek olayla değerlendirmek yanlıştır.',
        'Trafikte yaşanan stres <b>kaygıyı artırır, kalp atışını hızlandırır</b> ve saldırgan tutuma yol açabilir.',
        'Emisyonu yüksek egzoz dumanıyla araç kullanmak <b>doğaya, diğer canlılara ve bireylere karşı hak ihlalidir</b>.',
      ]),
    ],
  },
]

# ---------------------------------------------------------------- şablon ----

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-34HL041XN0"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-34HL041XN0');
</script>"""

FOOTER_CSS_YENI = """  .foot-wrap{max-width:1100px;margin:0 auto;padding:44px 28px 40px;display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:40px;align-items:start}
  .foot-hakkinda{display:flex;flex-direction:column;align-items:flex-start;gap:16px}
  .foot-hakkinda p{margin:0;font-size:14px;color:var(--muted);line-height:1.55;max-width:270px}
  .foot-col{display:flex;flex-direction:column;gap:10px}
  .foot-col h4{margin:0 0 4px;font-family:'Geist Mono',monospace;font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
  .foot-col a{color:var(--fg);font-size:14px;text-decoration:none}
  .foot-col a:hover{text-decoration:underline;text-underline-offset:3px}
  @media(max-width:860px){.foot-wrap{grid-template-columns:1fr 1fr;gap:30px}.foot-hakkinda{grid-column:1/-1}}"""

FOOTER_HTML_YENI = """  <footer class="site-footer">
    <div class="foot-wrap">
      <div class="foot-hakkinda">
        <a class="foot-marka" href="/">
          <img src="/assets/img/marka/logo.png" alt="">
          ehliyet.digital
        </a>
        <p>Sınavdan önce ders notlarını incele, hap bilgileri al ve deneme sınavları ile kendini test et. Ehliyet sınavına kolaylıkla hazırlan.</p>
        <a class="foot-feedback" href="mailto:omerlhn@gmail.com?subject=Ehliyet%20Deneme%20—%20Geri%20Bildirim">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          Geri bildirim gönder
        </a>
      </div>
      <nav class="foot-col" aria-label="Hap Bilgiler">
        <h4>Hap Bilgiler</h4>
        <a href="/hap-bilgiler/ilk-yardim/">İlk Yardım</a>
        <a href="/hap-bilgiler/trafik-ve-cevre/">Trafik ve Çevre</a>
        <a href="/hap-bilgiler/arac-teknigi/">Araç Tekniği</a>
        <a href="/hap-bilgiler/trafik-adabi/">Trafik Adabı</a>
      </nav>
      <nav class="foot-col" aria-label="Ders Notları">
        <h4>Ders Notları</h4>
        <a href="/dersler/ilk-yardim/ilk-yardim-ve-acil-tedavi/">İlk Yardım</a>
        <a href="/dersler/trafik-ve-cevre/temel-tanimlar/">Trafik ve Çevre</a>
        <a href="/dersler/arac-teknigi/motor-nedir/">Araç Tekniği</a>
        <a href="/dersler/trafik-adabi/temel-kavramlar/">Trafik Adabı</a>
      </nav>
      <nav class="foot-col" aria-label="Sayfalar">
        <h4>Sayfalar</h4>
        <a href="/hakkinda/">Hakkında</a>
        <a href="/iletisim/">İletişim</a>
        <a href="/gizlilik/">Gizlilik Politikası</a>
        <a href="/kullanim-sartlari/">Kullanım Şartları</a>
      </nav>
    </div>
  </footer>"""

ORTAK_CSS = """  :root{--fg:#08090a;--muted:#6a6f76;--line:#ececec;--bg:#fff}
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;font-family:'Inter',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    color:var(--fg);background:#fff;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;min-height:100vh;letter-spacing:-.011em}
  a{color:inherit}

  header{display:flex;align-items:center;gap:26px;height:64px;
    padding:0 max(28px, calc((100% - 1100px) / 2));border-bottom:1px solid var(--line);
    position:sticky;top:0;background:rgba(255,255,255,.8);backdrop-filter:saturate(180%) blur(10px);z-index:20}
  .nav{display:flex;gap:24px}
  .nav a{color:var(--muted);text-decoration:none;font-size:14px;font-weight:450;white-space:nowrap}
  .nav a:hover{color:var(--fg)}

  .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-family:inherit;font-weight:500;
    font-size:14px;line-height:1;text-decoration:none;cursor:pointer;border-radius:999px;padding:11px 20px;transition:.15s;white-space:nowrap;letter-spacing:-.01em}
  .btn-primary{background:#08090a;color:#fff;border:1px solid #08090a}
  .btn-primary:hover{background:#26282c;border-color:#26282c}
  .btn-outline{background:#fff;color:var(--fg);border:1px solid var(--line)}
  .btn-outline:hover{border-color:#c8c8c8;background:#fafafa}
  .btn-lg{padding:13px 26px;font-size:15px}

  main{flex:1}
  .eyebrow{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}

  /* Site footer */
  .site-footer{border-top:1px solid var(--line);background:#fafafa;margin-top:auto;padding:0}
{FOOTER_CSS}
  .foot-feedback{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line);background:#fff;border-radius:10px;padding:11px 18px;font-size:14px;font-weight:500;color:var(--fg);text-decoration:none;transition:.15s;white-space:nowrap}
  .foot-feedback:hover{border-color:#c8c8c8}
  .foot-feedback svg{color:var(--muted)}

  .marka{display:flex;align-items:center;flex-shrink:0;text-decoration:none}
  .marka img{width:26px;height:26px;object-fit:contain;display:block}
  .foot-marka{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--fg);
    font-size:14.5px;font-weight:600;letter-spacing:-.02em;flex-shrink:0}
  .foot-marka img{width:22px;height:22px;object-fit:contain;display:block}

  @media(max-width:640px){
    header{padding:0 16px;gap:12px;height:58px}
    .nav{gap:14px}
    .nav a{font-size:11px}
    .marka img{width:22px;height:22px}
    .foot-wrap{gap:26px}
  }""".replace("{FOOTER_CSS}", FOOTER_CSS_YENI)

HEADER_HTML = """  <header>
    <a class="marka" href="/" aria-label="ehliyet.digital"><img src="/assets/img/marka/logo.png" alt=""></a>
    <nav class="nav">
      <a href="/">Ana Sayfa</a>
      <a href="/dersler/">Ders Notları</a>
      <a href="/hap-bilgiler/">Hap Bilgiler</a>
    </nav>
  </header>"""

def head(baslik, aciklama, yol, ekstra_css):
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

{GTAG}
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="https://ehliyet.digital{yol}">

<!-- Open Graph (WhatsApp / Facebook / LinkedIn) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ehliyet Sınavı">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="https://ehliyet.digital{yol}">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="https://ehliyet.digital/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{baslik}">
<meta name="twitter:description" content="{aciklama}">
<meta name="twitter:image" content="https://ehliyet.digital/og-image.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{ORTAK_CSS}
{ekstra_css}
</style>
</head>
<body>

{HEADER_HTML}
"""

KUYRUK = f"""
{FOOTER_HTML_YENI}

  <script src="/assets/js/feedback.js" defer></script>
  <script type="module" src="/assets/js/auth-ui.js"></script>
</body>
</html>
"""

# ------------------------------------------------------- landing sayfası ----

LANDING_CSS = """
  /* Koyu hero — landing'in kimliği. Ana sayfa beyaz "vitrin", burası ürünün
     kendisi: renk dili ana sayfadaki yatay Hap Bilgiler kartından geliyor,
     ziyaretçi koyu karttan koyu sayfaya iner ve daha kaydırmadan
     örnek bilgileri görür. */
  .hero{background:#08090a;color:#fff;text-align:center}
  .hero-ic{max-width:1060px;margin:0 auto;padding:84px 28px 68px}
  .hero .eyebrow{color:#8a9097}
  .hero h1{margin:0 0 22px;font-size:clamp(44px,8vw,84px);font-weight:600;letter-spacing:-.032em;line-height:1.02}
  .hero .tanitim{margin:0 auto;font-size:19px;line-height:1.55;color:#b7bcc3;max-width:620px}
  .hero .tanitim b{color:#fff;font-weight:600}
  .stats{display:flex;justify-content:center;align-items:baseline;gap:16px;flex-wrap:wrap;margin:32px 0 0}
  .stat{font-family:'Geist Mono',monospace;font-size:13px;color:#8a9097;white-space:nowrap}
  .stat b{font-size:20px;font-weight:500;color:#fff;margin-right:7px}
  .stat-ayrac{color:#3a3d42}
  .ornekler{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:48px 0 0;text-align:left}
  .ornek{background:#131417;border:1px solid #26282c;border-radius:14px;padding:18px 20px}
  .ornek .kim{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#8a9097;margin:0 0 9px}
  .ornek p{margin:0;font-size:14px;line-height:1.55;color:#e6e8ea}

  .section{max-width:1100px;margin:0 auto;padding:88px 28px}
  .sec-title{margin:0 0 8px;font-size:clamp(28px,4vw,42px);font-weight:600;letter-spacing:-.03em;line-height:1.08}
  .sec-sub{margin:0 0 38px;font-size:16px;color:var(--muted);max-width:660px;line-height:1.6}

  .cat-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
  .cat-card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:16px;padding:24px;text-decoration:none;color:inherit;background:#fff;transition:.15s}
  a.cat-card:hover{border-color:#d4d4d4;box-shadow:0 12px 30px rgba(0,0,0,.06);transform:translateY(-3px)}
  .cat-top{display:flex;align-items:center;gap:14px;margin-bottom:14px}
  .cat-ico{width:44px;height:44px;flex-shrink:0;border:1px solid var(--line);border-radius:12px;display:flex;align-items:center;justify-content:center;color:var(--fg);background:#fafafa}
  .cat-card h3{margin:0;font-size:20px;font-weight:600;letter-spacing:-.02em}
  .cat-count{font-family:'Geist Mono',monospace;font-size:12px;color:var(--muted);margin-top:2px}
  .cat-on{list-style:none;margin:0 0 20px;padding:0;display:flex;flex-direction:column;gap:9px}
  .cat-on li{position:relative;padding-left:16px;font-size:14px;line-height:1.5;color:#3a3d42}
  .cat-on li::before{content:"";position:absolute;left:0;top:.62em;width:7px;height:2px;border-radius:2px;background:#d0d4da}
  .cat-go{margin-top:auto;display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:500;color:var(--fg)}
  a.cat-card:hover .cat-go{gap:9px}

  .cta{max-width:1100px;margin:0 auto;padding:0 28px 96px}
  .cta-inner{border:1px solid var(--line);border-radius:24px;background:#fafafa;padding:64px 32px;text-align:center}
  .cta-inner h2{margin:0 0 14px;font-size:clamp(28px,4vw,44px);font-weight:600;letter-spacing:-.03em;line-height:1.06}
  .cta-inner p{margin:0 auto 30px;font-size:17px;color:var(--muted);max-width:460px;line-height:1.5}

  @media(max-width:860px){.cat-grid{grid-template-columns:1fr}.ornekler{grid-template-columns:1fr}}
  @media(max-width:640px){.hero-ic{padding:56px 20px 44px}.hero .tanitim{font-size:17px}.stats{gap:12px}.ornekler{margin-top:38px}.section{padding:60px 22px}.cta-inner{padding:44px 22px}}"""

# Koyu hero'da gösterilen örnek bilgiler: sayfanın değeri daha kaydırmadan
# görünsün diye. Kartlardaki on_izleme'lerden farklı bilgiler seçildi.
HERO_ORNEKLER = [
  ("Trafik ve Çevre", "Gece kısa farla net görüş mesafesi ortalama 25 metredir."),
  ("İlk Yardım", "Temel yaşam desteği 30 kalp masajı + 2 yapay solunumdur ve kalp masajıyla başlanır."),
  ("Araç Tekniği", "Şarj ve yağ basıncı lambaları yanarsa araç derhal durdurulur, kontak kapatılır."),
]

def landing():
    toplam = sum(len(f) for d in DERSLER for _, f in d["gruplar"])
    ornekler_html = "\n".join(
        f"""          <div class="ornek"><p class="kim">{ders}</p><p>{bilgi}</p></div>"""
        for ders, bilgi in HERO_ORNEKLER)
    kartlar = []
    for d in DERSLER:
        adet = sum(len(f) for _, f in d["gruplar"])
        kalan = adet - len(d["on_izleme"])
        onizleme = "\n".join(f"            <li>{b}</li>" for b in d["on_izleme"])
        kartlar.append(f"""        <a class="cat-card" href="/hap-bilgiler/{d['slug']}/">
          <div class="cat-top">
            <span class="cat-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d['ikon']}</svg></span>
            <div><h3>{d['ad']}</h3><div class="cat-count">{adet} hap bilgi</div></div>
          </div>
          <ul class="cat-on">
{onizleme}
          </ul>
          <span class="cat-go">+{kalan} bilgi daha →</span>
        </a>""")
    kartlar_html = "\n\n".join(kartlar)

    govde = f"""
  <main>
    <!-- HERO -->
    <section class="hero">
      <div class="hero-ic">
        <p class="eyebrow">Sınavdan önce son tekrar</p>
        <h1>Hap Bilgiler</h1>
        <p class="tanitim">Uzun anlatım yok. Deneme sınavlarındaki soruları çözdüren <b>{toplam} bilgi</b>, dört ders altında tek tek damıtıldı — oku, aklında tut, sınavda uygula.</p>
        <div class="stats">
          <span class="stat"><b>{toplam}</b>hap bilgi</span>
          <span class="stat-ayrac">·</span>
          <span class="stat"><b>{len(DERSLER)}</b>ders</span>
          <span class="stat-ayrac">·</span>
          <span class="stat"><b>~15 dk</b>tekrar</span>
        </div>
        <div class="ornekler">
{ornekler_html}
        </div>
      </div>
    </section>

    <!-- DERSLER -->
    <section class="section">
      <p class="eyebrow">Dersler</p>
      <h2 class="sec-title">Sınavlık bilgiler</h2>
      <p class="sec-sub">Hap bilgi, bir sınav sorusunu çözmeye yeten tek cümledir: bir mesafe, bir süre, bir sıralama ya da bir kural. Buradaki {toplam} bilginin her biri deneme sınavlarındaki sorulardan damıtıldı ve ders sayfalarında konuya göre gruplandı — sınavdan hemen önce hızlı tekrar için birebir.</p>
      <div class="cat-grid">

{kartlar_html}

      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="cta-inner">
        <h2>Bilgileri sınavda test et</h2>
        <p>Hap bilgileri okuduysan sıra denemede: gerçek e-sınav formatında 50 soruyla kendini ölç.</p>
        <a class="btn btn-primary btn-lg" href="/panel/?g=sinavlar" data-korumali>Giriş Yap ve Sınava Başla</a>
      </div>
    </section>

  </main>
"""
    return head(
        "Hap Bilgiler — Ehliyet Sınavına Hızlı Hazırlık",
        f"Ehliyet sınavına hızlı hazırlık: deneme sınavlarındaki soruları çözdüren {toplam} hap bilgi. İlk Yardım, Trafik ve Çevre, Araç Tekniği ve Trafik Adabı.",
        "/hap-bilgiler/",
        LANDING_CSS,
    ) + govde + KUYRUK

# ---------------------------------------------------------- ders sayfası ----

DERS_CSS = """
  /* Eyebrow + başlık boşlukları /dersler/ sayfasındaki "Tüm Dersler" ile birebir:
     eyebrow altı 12px, başlık clamp(28-40px) ve varsayılan satır yüksekliği.
     Daha büyük punto + sıkı line-height, İ'nin noktasını eyebrow'a değdiriyordu. */
  .hero{max-width:1100px;margin:0 auto;padding:72px 28px 48px}
  .hero h1{margin:0 0 16px;font-size:clamp(28px,4vw,40px);font-weight:600;letter-spacing:-.03em}
  .hero p{margin:0;font-size:16px;line-height:1.6;color:var(--muted);max-width:640px}

  .icerik{max-width:1100px;margin:0 auto;padding:0 28px 40px}
  .grup{padding:26px 0 6px}
  .grup h2{margin:0 0 18px;font-size:22px;font-weight:600;letter-spacing:-.025em}
  .hap-list{display:flex;flex-direction:column;gap:12px}
  .hap{display:flex;gap:16px;align-items:flex-start;border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff;font-size:15px;line-height:1.62}
  .hap b{font-weight:600}
  .hap-num{font-family:'Geist Mono',monospace;font-size:12.5px;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:6px 9px;flex-shrink:0}
  a.hap-num{text-decoration:none;transition:.12s}
  a.hap-num:hover{color:var(--fg);border-color:#c8c8c8;background:#fafafa}
  .hap-detay{margin-left:auto;align-self:center;flex-shrink:0;font-size:13px;color:var(--muted);text-decoration:none;white-space:nowrap}
  .hap-detay:hover{color:var(--fg);text-decoration:underline}
  @media(max-width:640px){.hap{flex-wrap:wrap}.hap-detay{margin-left:0;width:100%;padding-left:0}}

  .cta{max-width:1100px;margin:0 auto;padding:48px 28px 96px}
  .cta-inner{border:1px solid var(--line);border-radius:24px;background:#fafafa;padding:52px 32px;text-align:center}
  .cta-inner h2{margin:0 0 12px;font-size:clamp(26px,4vw,38px);font-weight:600;letter-spacing:-.03em;line-height:1.08}
  .cta-inner p{margin:0 auto 28px;font-size:16px;color:var(--muted);max-width:460px;line-height:1.5}
  .cta-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}

  @media(max-width:640px){.hero{padding:52px 20px 40px}.icerik{padding:0 20px 28px}.cta{padding:36px 20px 72px}.cta-inner{padding:40px 22px}}"""

def ders_sayfasi(d):
    adet = sum(len(f) for _, f in d["gruplar"])
    parcalar = []
    haplar = iter(hap_listesi(d))
    for grup_ad, bilgiler in d["gruplar"]:
        maddeler = []
        for _ in bilgiler:
            sira, _g, b, _duz, slug = next(haplar)
            # Numara, hap bilginin kendi sayfasına link (tools/hap-sayfa-uret.py üretir).
            maddeler.append(f"""        <div class="hap"><a class="hap-num" href="/hap-bilgiler/{d['slug']}/{slug}/" aria-label="Hap bilgi {sira:02d} sayfası">{sira:02d}</a><span>{b}</span><a class="hap-detay" href="/hap-bilgiler/{d['slug']}/{slug}/">Detay &rarr;</a></div>""")
        maddeler_html = "\n".join(maddeler)
        parcalar.append(f"""      <section class="grup">
        <h2>{grup_ad}</h2>
        <div class="hap-list">
{maddeler_html}
        </div>
      </section>""")
    gruplar_html = "\n\n".join(parcalar)

    govde = f"""
  <main>
    <section class="hero">
      <p class="eyebrow">Hap Bilgiler</p>
      <h1>{d['ad']}</h1>
      <p>{d['ad']} ile ilgili hap bilgileri öğren, sınavdaki soruları rahatlıkla çöz. Hap bilgilerin tamamı aşağıda!</p>
    </section>

    <div class="icerik">
{gruplar_html}
    </div>

    <section class="cta">
      <div class="cta-inner">
        <h2>Bu bilgilerle kendini test et</h2>
        <p>{d['ad']} soruları deneme sınavında seni bekliyor. Konuyu derinlemesine çalışmak istersen ders notları da hazır.</p>
        <div class="cta-actions">
          <a class="btn btn-primary btn-lg" href="/panel/?g=sinavlar" data-korumali>Giriş Yap ve Sınava Başla</a>
          <a class="btn btn-outline btn-lg" href="{d['ders_link']}">{d['ad']} Ders Notları</a>
        </div>
      </div>
    </section>

  </main>
"""
    return head(
        f"{d['ad']} Hap Bilgiler — Ehliyet Sınavı",
        f"Ehliyet sınavı {d['ad']} hap bilgileri: {d['ozet'].rstrip('.')}. {adet} bilgi tek sayfada.",
        f"/hap-bilgiler/{d['slug']}/",
        DERS_CSS,
    ) + govde + KUYRUK

# ------------------------------------------------------ footer güncelleme ----

ESKI_CSS = """  .foot-wrap{max-width:1100px;margin:0 auto;padding:22px 28px;display:flex;align-items:center;gap:24px;flex-wrap:wrap}
  .foot-links{display:flex;align-items:center;gap:26px;flex-wrap:wrap}
  .foot-links a{color:var(--fg);font-size:14px;text-decoration:underline;text-underline-offset:3px;text-decoration-color:#c9ccd1}
  .foot-links a:hover{text-decoration-color:var(--fg)}
  .foot-feedback{margin-left:auto;"""

YENI_CSS = FOOTER_CSS_YENI + "\n  .foot-feedback{"

ESKI_MEDYA = ".foot-wrap{gap:16px}.foot-feedback{margin-left:0}"
YENI_MEDYA = ".foot-wrap{gap:26px}"

ESKI_FOOTER = """  <footer class="site-footer">
    <div class="foot-wrap">
      <a class="foot-marka" href="/">
        <img src="/assets/img/marka/logo.png" alt="">
        ehliyet.digital
      </a>
      <nav class="foot-links">
        <a href="/gizlilik/">Gizlilik Politikası</a>
        <a href="/kullanim-sartlari/">Kullanım Şartları</a>
        <a href="/hakkinda/">Hakkında</a>
        <a href="/iletisim/">İletişim</a>
      </nav>
      <a class="foot-feedback" href="mailto:omerlhn@gmail.com?subject=Ehliyet%20Deneme%20—%20Geri%20Bildirim">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Geri bildirim gönder
      </a>
    </div>
  </footer>"""

SAYFALAR = ["index.html", "dersler/index.html", "hakkinda/index.html",
            "iletisim/index.html", "gizlilik/index.html", "kullanim-sartlari/index.html"]

def footer_guncelle():
    for yol in SAYFALAR:
        tam = os.path.join(KOK, yol)
        icerik = open(tam, encoding="utf-8").read()
        # Sütunlu footer zaten kuruluysa dokunma; script yeniden çalıştırılabilir kalsın.
        if FOOTER_HTML_YENI in icerik:
            print(f"footer zaten güncel: {yol}")
            continue
        for eski, yeni, ad in [(ESKI_CSS, YENI_CSS, "css"),
                               (ESKI_MEDYA, YENI_MEDYA, "medya"),
                               (ESKI_FOOTER, FOOTER_HTML_YENI, "html")]:
            n = icerik.count(eski)
            if n != 1:
                sys.exit(f"HATA: {yol} içinde '{ad}' bloğu {n} kez bulundu (1 bekleniyordu)")
            icerik = icerik.replace(eski, yeni)
        open(tam, "w", encoding="utf-8").write(icerik)
        print(f"footer güncellendi: {yol}")

def sayfalari_yaz():
    hedef = os.path.join(KOK, "hap-bilgiler")
    os.makedirs(hedef, exist_ok=True)
    open(os.path.join(hedef, "index.html"), "w", encoding="utf-8").write(landing())
    print("yazıldı: hap-bilgiler/index.html")
    for d in DERSLER:
        klasor = os.path.join(hedef, d["slug"])
        os.makedirs(klasor, exist_ok=True)
        open(os.path.join(klasor, "index.html"), "w", encoding="utf-8").write(ders_sayfasi(d))
        adet = sum(len(f) for _, f in d["gruplar"])
        print(f"yazıldı: hap-bilgiler/{d['slug']}/index.html ({adet} hap bilgi)")

if __name__ == "__main__":
    sayfalari_yaz()
    footer_guncelle()
    print("tamam")
