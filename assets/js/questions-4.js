// MTSK E-Sınav — Sınav 4 (50 soru). Cevaplar: correct 0=A,1=B,2=C,3=D
// Kaynak: 21.04.2018 MTSK sınavı K kitapçığı ekran görüntüleri + cevap anahtarı
// media.file yoksa/klasörde bulunamazsa caption (açıklama) gösterilir; dosya eklenince otomatik görünür.
window.QUESTIONS = [
  { n:1, section:"İlk Yardım",
    stem:`I. Kazazedenin tedavi edilmesi
II. Hayati tehlikenin ortadan kaldırılması
III. Yaşamsal fonksiyonların sürdürülmesinin sağlanması

Yukarıdakilerden hangileri ilk yardımın öncelikli amaçlarındandır?`,
    options:[`I ve II.`,`I ve III.`,`II ve III.`,`I, II ve III.`], correct:2 },

  { n:2, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi solunum sistemi organlarındandır?`,
    options:[`Kalp`,`Akciğerler`,`Pankreas`,`Böbrekler`], correct:1 },

  { n:3, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi "kaza sonuçlarının ağırlaşmasını önlemek için olay yerinin değerlendirilmesi" işlemini kapsar?`,
    options:[`Koruma`,`Bildirme`,`Kurtarma`,`Tedavi etme`], correct:0 },

  { n:4, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi kalp durmasının belirtilerindendir?`,
    options:[`Aşırı hareketlilik`,`Bilincin açık olması`,`Kalp atımının olmaması`,`Hızlı ve yüzeysel solunum`], correct:2 },

  { n:5, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi bebeklere yapılan yapay solunum uygulamasında, ilk yardımcının dikkat etmesi gereken kurallardandır?`,
    options:[`Bebeğin yumuşak bir zemin üzerine sırtüstü yatırılması`,`Hava yolu tıkanıklığına neden olan yabancı cisim varsa bebeğin yutmasının sağlanması`,`Bebeğin solunum yapıp yapmadığının bak-dinle-hisset yöntemiyle 2 dakika süre ile kontrol edilmesi`,`Bebekte solunum yoksa ağız dolusu nefes alınması ve ağzın, bebeğin ağız ve burnunu içine alacak şekilde yerleştirilmesi`], correct:3 },

  { n:6, section:"İlk Yardım",
    stem:`Solunum yolu yabancı bir cisimle tıkanmış olan kazazede öksürüyor, nefes alabiliyor ve konuşabiliyorsa bu kazazedede aşağıdakilerden hangisinin olduğu düşünülür?`,
    options:[`Koma`,`Kısmi tıkanma`,`Tam tıkanma`,`Solunum durması`], correct:1 },

  { n:7, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi şok belirtilerinden biri değildir?`,
    options:[`Huzursuzluk`,`Baş dönmesi`,`Dudak çevresinde morarma`,`Ciltte ısı artışı, kızarıklık ve kuruluk`], correct:3 },

  { n:8, section:"İlk Yardım",
    stem:`Burun kanaması olan kazazedeye yapılması gereken ilk yardım uygulaması hangisidir?`,
    options:[`Burun kanatlarının 5 dakika süre ile sıkılması`,`Yan yatış pozisyonuna getirilmesi`,`Başının geriye doğru itilmesi`,`Sırtüstü yatırılması`], correct:0 },

  { n:9, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi delici göğüs yaralanmalarında kazazedeye yapılan doğru bir ilk yardım uygulamasıdır?`,
    options:[`Ayaklarının yüksekte tutulup yüzüstü yatırılması`,`Bilinci açık ise yarı oturur duruma getirilmesi`,`Ağızdan ılık içecekler verilmesi`,`Batan cismin çıkarılması`], correct:1 },

  { n:10, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi burkulmalarda yapılması gereken ilk yardım uygulamalarındandır?`,
    options:[`Sıkıştırıcı bir bandajla burkulan eklemin tespit edilmesi`,`Şişliği azaltmak için bölgenin vücut seviyesinden aşağıya indirilmesi`,`Burkulan eklem yüzeyinin sürekli hareket ettirilmesi`,`Boğucu sargı (turnike) uygulanması`], correct:0 },

  { n:11, section:"İlk Yardım",
    stem:`Koma durumundaki kazazedeye aşağıdaki pozisyonlardan hangisi verilmelidir?`,
    options:[`Şok pozisyonu`,`Sırtüstü yatış pozisyonu`,`Yarı yüzükoyun-yan pozisyon`,`Baş geride yarı oturuş pozisyonu`], correct:2 },

  { n:12, section:"İlk Yardım",
    stem:`Aşağıdakilerden hangisi kazazedenin taşınmasında uyulması gereken genel kurallardandır?`,
    options:[`İlk yardımcının kendi sağlığını riske sokması`,`İlk yardımcının kalkarken ağırlığı karın kaslarına vermesi`,`Kazazedenin mümkün olduğunca çok hareket ettirilmesi`,`Kazazedenin baş-boyun-gövde ekseni esas alınarak en az 6 destek noktasından kavranması`], correct:3 },

  { n:13, section:"Trafik ve Çevre",
    stem:`I. Hoşgörülü olunması
II. Bencillikten uzak durulması
III. Olaylara aşırı tepki gösterilmesi

Trafik ortamını paylaşanlarda, yukarıda verilen tutum ve davranışlardan hangilerinin bulunması hâlinde trafik düzeni ve güvenliği olumlu yönde etkilenir?`,
    options:[`Yalnız I.`,`I ve II.`,`II ve III.`,`I, II ve III.`], correct:1 },

  { n:14, section:"Trafik ve Çevre",
    stem:`Aşağıdakilerden hangisi Karayolları Genel Müdürlüğünün görevlerinden biri değildir?`,
    options:[`Şehir içindeki açık ve kapalı otoparklara izin vermek`,`Kara yollarındaki hız sınırlarını belirleyip işaretlemek`,`Kara yollarındaki işaretleme standartlarını tespit ve kontrol etmek`,`Kara yolu güvenliğini ilgilendiren konulardaki projeleri incelemek ve onaylamak`], correct:0 },

  { n:15, section:"Trafik ve Çevre",
    stem:`Trafik zabıtası veya yetkililerce Kanunda ve yönetmelikte belirtilen hâllerde araçla ilgili belgelerin alınması ve aracın belirli bir yere çekilerek trafikten alıkonulmasına ne denir?`,
    options:[`Trafik suçu`,`Trafik terörü`,`Trafik kusuru`,`Trafikten men`], correct:3 },

  { n:16, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru16.png"},
    caption:`Kolunu yere paralel uzatmış, elini aşağı yukarı sallayan trafik görevlisi.`,
    stem:`Şekildeki trafik görevlisinin yapmış olduğu işaretin sürücüler için anlamı nedir?`,
    options:[`Dur`,`Hızlan`,`Yavaşla`,`Sağa yanaş`], correct:2 },

  { n:17, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru17.png"},
    caption:`Kırmızı kenarlı üçgen içinde çanta taşıyan iki çocuğun bulunduğu trafik işareti.`,
    stem:`Şekildeki trafik işareti aşağıdakilerden hangisine yaklaşıldığını bildirir?`,
    options:[`Okul geçidine`,`Yürüyüş yoluna`,`Gençlik kampına`,`Alt veya üst geçitlere`], correct:0 },

  { n:18, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru18.png"},
    caption:`Kırmızı kenarlı üçgen içinde araç tekerleğinden sıçrayan taşların gösterildiği gevşek malzemeli zemin işareti.`,
    stem:`Şekildeki tehlike uyarı işaretini gören sürücü aşağıdakilerden hangisini yapmalıdır?`,
    options:[`Banketten gitmeli`,`Takip mesafesini artırmalı`,`Hızını artırarak öndeki aracı geçmeli`,`Acil uyarı ışıklarını yakarak derhâl durmalı`], correct:1 },

  { n:19, section:"Trafik ve Çevre",
    stem:`Aşağıdaki trafik işaretlerinden hangisi öndeki taşıtı geçme yasağının sona erdiğini bildirir?`,
    optionImages:["/assets/img/sinav-4/soru19a.png","/assets/img/sinav-4/soru19b.png","/assets/img/sinav-4/soru19c.png","/assets/img/sinav-4/soru19d.png"],
    options:[`A`,`B`,`C`,`D`], correct:0 },

  { n:20, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru20.png"},
    caption:`Kırmızı çember içinde kamyon bulunan trafik işareti.`,
    stem:`Şekildeki trafik işareti aşağıdakilerden hangisini bildirir?`,
    options:[`Kamyon garajını`,`Kamyonun giremeyeceğini`,`Kamyon için geçme yasağının sona erdiğini`,`Kamyon için azami hız sınırlaması olduğunu`], correct:1 },

  { n:21, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru21.png"},
    caption:`Üç şeritli yolda şeritler üzerine çizilmiş sola dönüş, ileri ve sağa dönüş okları.`,
    stem:`Kavşaklara yaklaşırken yol üzerine çizilmiş şekildeki oklar sürücülere neyi bildirir?`,
    options:[`Hızın artırılması gerektiğini`,`Sağa ve sola dönülemeyeceğini`,`Seyir yönüne uygun şeridin kullanılması gerektiğini`,`Durma, duraklama ve park etmenin yasaklanmış olduğunu`], correct:2 },

  { n:22, section:"Trafik ve Çevre",
    stem:`Aşağıdaki hâllerin hangisinde sürücü araç kullanmaktan men edilir?`,
    options:[`Taşıma sınırının üstünde yolcu almışsa`,`Taşıma sınırının üstünde yük yüklemişse`,`Uyuşturucu madde alarak araç kullanıyorsa`,`Zorunlu mali sorumluluk sigortasını yaptırmamışsa`], correct:2 },

  { n:23, section:"Trafik ve Çevre",
    stem:`I. Aracın yük ve teknik özelliğine
II. Görüş, yol, hava ve trafik durumuna
III. Aracın cinsine uygun hız sınırlamalarına

Sürücüler, araçlarının hızını yukarıdakilerden hangilerine göre ayarlamak zorundadır?`,
    options:[`Yalnız I.`,`I ve II.`,`II ve III.`,`I, II ve III.`], correct:3 },

  { n:24, section:"Trafik ve Çevre",
    stem:`Öndeki aracın güvenle takip edildiği uzaklığa ne denir?`,
    options:[`Takip mesafesi`,`Geçiş mesafesi`,`Görüş mesafesi`,`İntikal mesafesi`], correct:0 },

  { n:25, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru25.png"},
    caption:`İki yönlü yolda yan yana çizilmiş kesik ve devamlı yol çizgileri ile seyreden araçlar.`,
    stem:`Şekildeki kara yolu bölümünde, yan yana çizilmiş kesik ve devamlı yol çizgileri sürücülere aşağıdakilerden hangisini bildirir?`,
    options:[`Çift yönlü yoldan tek yönlü yola girileceğini`,`Her iki yönde seyreden araçların bölünmüş yola gireceğini`,`Her iki yönde seyreden araçların şerit değiştiremeyeceğini`,`Devamlı çizgi tarafındaki araçların şerit değiştiremeyeceğini`], correct:3 },

  { n:26, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru26.png"},
    caption:`Dönel kavşağa yaklaşan araç ve 1, 2, 3 olarak numaralanmış şeritler.`,
    stem:`Şekildeki aracın sürücüsü, dönel kavşaktan geriye dönüş yapmak için hangi şeridi izlemelidir?`,
    options:[`İstediği şeridi`,`1 numaralı şeridi`,`2 numaralı şeridi`,`3 numaralı şeridi`], correct:1 },

  { n:27, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-4/soru27.png"},
    caption:`Kontrolsüz kavşakta karşılaşan 1, 2 ve 3 numaralı araçlar; 1 numaralı araç sola dönmektedir.`,
    stem:`Şekildeki gibi kontrolsüz kavşakta karşılaşan araçların geçiş hakkı sıralaması nasıl olmalıdır?`,
    options:[`1 - 2 - 3`,`2 - 1 - 3`,`3 - 1 - 2`,`3 - 2 - 1`], correct:3 },

  { n:28, section:"Trafik ve Çevre",
    stem:`Aşağıdakilerden hangisi geçiş üstünlüğüne sahip araçlardandır?`,
    options:[`İtfaiye aracı`,`Motosiklet`,`Tarım traktörü`,`Toplu taşıma aracı`], correct:0 },

  { n:29, section:"Trafik ve Çevre",
    stem:`Park edilen araç için aşağıdakilerden hangisinin yapılmasına gerek yoktur?`,
    options:[`El freninin çekilmesine`,`Motorunun durdurulmasına`,`Acil uyarı ışıklarının yakılmasına`,`Yol eğimli ise uygun vitese takılmasına`], correct:2 },

  { n:30, section:"Trafik ve Çevre",
    stem:`Geceleyin önündeki aracı geçmek isteyen sürücü, bu araçla yan yana gelinceye kadar hangi ışıkları kullanmalıdır?`,
    options:[`Sis ışıklarını`,`Acil uyarı ışıklarını`,`Uzağı gösteren ışıkları`,`Yakını gösteren ışıkları`], correct:3 },

  { n:31, section:"Trafik ve Çevre",
    stem:`Kamyon, kamyonet ve römorklarda yükle birlikte yolcu taşınırken aşağıdakilerden hangisinin yapılması yasaktır?`,
    options:[`Yüklerin bağlanması`,`Yolcuların yüklerin üzerine oturtulması`,`Kasanın yan ve arka kapaklarının kapatılması`,`Yolcuların kasa içinde ayrılmış bir yere oturtulması`], correct:1 },

  { n:32, section:"Trafik ve Çevre",
    stem:`Araçlarda emniyet kemeri kullanımının zorunlu olması ile aşağıdakilerden hangisi hedeflenmektedir?`,
    options:[`Kazaların önlenmesi`,`Sürücülerin dikkatinin artırılması`,`Denetimlerde herhangi bir sorun yaşanmaması`,`Kaza anında ölüm ve yaralanmaların en aza indirilmesi`], correct:3 },

  { n:33, section:"Trafik ve Çevre",
    stem:`Aşağıdakilerden hangisi trafik kazalarının en önemli sebebidir?`,
    options:[`Trafik görevlisi sayısının yetersiz olması`,`Uyarı işaretlerinin yetersiz olması`,`Sürücülerin kurallara uymaması`,`Yolların bakımsız olması`], correct:2 },

  { n:34, section:"Trafik ve Çevre",
    stem:`Aşağıdakilerden hangisi sürüş güvenliğini olumsuz yönde etkiler?`,
    options:[`Viraja girmeden önce hızı artırmak`,`Aracı kullanırken yola konsantre olmak`,`Yüksek hızlarda ani manevra yapmaktan kaçınmak`,`Her hızda, fren için ne kadar duruş mesafesi olduğunu hesaplamayı öğrenmek`], correct:0 },

  { n:35, section:"Trafik ve Çevre",
    stem:`Aşağıdakilerden hangisi çevre kirliliğini önleyici tedbirlerden biri değildir?`,
    options:[`Kısa mesafeli yerlere yürüyerek gidilmesi`,`İniş eğimli yollarda motorun durdurulması`,`Trafiğin yoğun olmadığı taşıt yollarının seçilmesi`,`Mümkün olduğunca toplu taşıma araçlarının kullanılması`], correct:1 },

  { n:36, section:"Araç Tekniği",
    stem:`Aşağıdakilerden hangisi aracı istenilen yöne sevk eder?`,
    options:[`Marş sistemi`,`Yağlama sistemi`,`Direksiyon sistemi`,`Aydınlatma sistemi`], correct:2 },

  { n:37, section:"Araç Tekniği",
    stem:`I. LPG
II. Benzin
III. Motorin

İçten yanmalı motorlarda yukarıdaki yakıtlardan hangileri kullanılır?`,
    options:[`Yalnız I.`,`I ve II.`,`II ve III.`,`I, II ve III.`], correct:3 },

  { n:38, section:"Araç Tekniği",
    stem:`Aşağıdakilerden hangisi aracı kullanmaya başlamadan önce yapılması gereken hazırlıklardan biri değildir?`,
    options:[`Klimanın açılması`,`Koltuğun ayarlanması`,`Aynaların ayarlanması`,`Emniyet kemerinin takılması`], correct:0 },

  { n:39, section:"Araç Tekniği",
    stem:`Aracın gösterge panelinde aşağıdaki ikaz ışıklarından hangisinin yanıyor olması araç yakıtının bitmek üzere olduğunu bildirir?`,
    optionImages:["/assets/img/sinav-4/soru39a.png","/assets/img/sinav-4/soru39b.png","/assets/img/sinav-4/soru39c.png","/assets/img/sinav-4/soru39d.png"],
    options:[`A`,`B`,`C`,`D`], correct:2 },

  { n:40, section:"Araç Tekniği",
    stem:`Motorlu araçlarda motorun yağ seviyesini kontrol etmeye yarayan ve özel işaretleri bulunan parçaya ne ad verilir?`,
    options:[`Yağdanlık`,`Yağ çubuğu`,`Yağ filtresi`,`Yağ pompası`], correct:1 },

  { n:41, section:"Araç Tekniği",
    stem:`Aracın elektrik devresinde, akım yüksek olduğunda eriyerek güvenliği sağlayan parça aşağıdakilerden hangisidir?`,
    options:[`Akü`,`Platin`,`Sigorta`,`Alternatör`], correct:2 },

  { n:42, section:"Araç Tekniği",
    stem:`Kriko ile aracı kaldırırken tekerleklere takoz konulmasının nedeni aşağıdakilerden hangisidir?`,
    options:[`Aracın motorunu çalıştırabilmek`,`Aracın hareket etmesini engellemek`,`Araç yakıtının buharlaşmasını engellemek`,`Araç motorunun sarsıntısız çalışmasını sağlamak`], correct:1 },

  { n:43, section:"Araç Tekniği",
    stem:`Seyir hâlindeyken araçtan "sürekli yakıt kokusu" alınması durumunda aşağıdakilerden hangisi yapılır?`,
    options:[`Antifriz kontrol edilir.`,`Önemsenmez yola devam edilir.`,`Lastiklerin hava basıncı kontrol edilir.`,`Trafik kurallarına uyarak durulur ve kontak kapatılır.`], correct:3 },

  { n:44, section:"Araç Tekniği",
    stem:`Aşağıdakilerden hangisi yakıt tüketiminin artmasında sürücüden kaynaklanan kusurdur?`,
    options:[`Aşırı hız yapılması`,`Frenlerin ayarsız olması`,`Rölanti ayarının bozuk olması`,`Lastiklerin havasının az olması`], correct:0 },

  { n:45, section:"Trafik Adabı",
    stem:`I. Trafikteki bütün kuralların nedenini öğrenir.
II. Araç kullanırken yapacağı bir kural ihlalinin sonucunda sadece maddi ceza olduğunu düşünür.
III. Trafik içinde yapacağı bir kural ihlalinde, kendisinin ya da sevdiklerinin canını tehlikeye attığının farkında değildir.

Yukarıdakilerden hangileri trafik adabına sahip olan bir sürücü için söylenebilir?`,
    options:[`Yalnız I.`,`I ve II.`,`II ve III.`,`I, II ve III.`], correct:0 },

  { n:46, section:"Trafik Adabı",
    stem:`Ailesi ile birlikte yolculuk yapan bir sürücü, aracını hız limitlerini aşarak sürdüğünde ailesinin hayatını da tehlikeye atmış olacaktır.

Bu sürücü, hız ihlalinden kaynaklanan olası bir kazada sevdiklerinin canını riske atmakla trafikte aşağıdaki değerlerden hangisini yerine getirmemiş olur?`,
    options:[`Hırçınlık`,`Bencillik`,`Sorumluluk`,`Hoşnutsuzluk`], correct:2 },

  { n:47, section:"Trafik Adabı",
    stem:`Öndeki araç yol kenarına park etmeye çalışırken arkadan gelen diğer aracın onu beklemesi durumu, trafikte aşağıdaki değerlerden hangisine sahip olunduğunu gösterir?`,
    options:[`Öfke`,`Sabır`,`İnatlaşma`,`Aşırı tepki`], correct:1 },

  { n:48, section:"Trafik Adabı",
    stem:`Aşağıdaki değerlerden hangisine sahip olan sürücü, yoğun trafikte bir dizi hâlinde gitmekte olan diğer sürücülerin önlerine geçip trafiği daha da sıkışık hâle getirerek yoluna devam etmez?`,
    options:[`Bencil`,`Sorumsuz`,`Görgü seviyesi düşük`,`Empati düzeyi yüksek`], correct:3 },

  { n:49, section:"Trafik Adabı",
    stem:`Seyir hâlindeki sürücünün, yaptığı bir hatadan dolayı eliyle veya yüz ifadesiyle diğer sürücülerden özür dilemesi trafikte aşağıdakilerden hangisinin kullanıldığına örnek olur?`,
    options:[`Beden dilinin`,`Bencilliğin`,`İnatlaşmanın`,`Tahammülsüzlüğün`], correct:0 },

  { n:50, section:"Trafik Adabı",
    stem:`Aşağıdakilerden hangisi trafikte bireye yapılan hak ihlallerindendir?`,
    options:[`Aşırı hız yapmaktan kaçınılması`,`Geçiş önceliğine sahip araçlara yol verilmesi`,`Trafikte sürücülerin tek başına olmadığının düşünülmesi`,`Engeli olmadığı hâlde engelli kişiler için ayrılmış yerlere park edilmesi`], correct:3 },
];
