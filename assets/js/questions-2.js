// MTSK E-Sınav — Sınav 2 (50 soru). Cevaplar: correct 0=A,1=B,2=C,3=D
// Kaynak: Sınav_2/Sorular ekran görüntüleri + Sınav_2_Cevap_Anahtarı.pdf
// media.file yoksa/klasörde bulunamazsa caption (açıklama) gösterilir; dosya eklenince otomatik görünür.
window.QUESTIONS = [
  { n:1, section:"İlk Yardım",
    stem:`Sinir sistemine aittir ve omurga kanalı içinde, boyundan başlayıp kuyruk sokumuna kadar uzanır. Bu organ beyin ve vücut arasında bağlantıyı sağlar ve reflekslerin merkezidir.

Bu bilgi, hangi organa aittir?`,
    options:[`Beyin`,`Beyincik`,`Omurilik`,`Omurilik soğanı`], correct:2 },

  { n:2, section:"İlk Yardım",
    stem:`Baş veya omurga yaralanması olmayan bilinci kapalı yaralıya, hava yolu açıklığını sağlamak için hangi pozisyon verilmelidir?`,
    optionImages:["/assets/img/sinav-2/soru2a.png","/assets/img/sinav-2/soru2b.png","/assets/img/sinav-2/soru2c.png","/assets/img/sinav-2/soru2d.png"],
    options:[`A`,`B`,`C`,`D`], correct:1 },

  { n:3, section:"İlk Yardım",
    media:{type:"image", file:"/assets/img/sinav-2/soru3.jpeg"},
    caption:`Bebeklerde Heimlich manevrasının I, II, III, IV olarak numaralanmış dört uygulama aşaması.`,
    stem:`Görselde bebeklerde ilk yardım olarak uygulanan Heimlich manevrasının uygulama aşamaları karışık olarak verilmiştir.

Buna göre, sıralamanın doğru olması için numaralanmış aşamalardan hangileri yer değiştirmelidir?`,
    options:[`I ve II`,`I ve IV`,`II ve III`,`III ve IV`], correct:1 },

  { n:4, section:"İlk Yardım",
    stem:`Olay yerindeki ilk yardımcının, bilinçleri kapalı ve solunumu olmayan dört farklı kazazedeye ilişkin tespitleri tabloda verilmiştir.

Kazazede — Tespit Edilen Durum
I. Ağız ve çevresinde yaralanma
II. Bacakta açık kırık ve yaralanma
III. Göz çevresinde morluk ve kulağında kanama
IV. Karın gölgesinde vücut eksenine dik olan açık yara

Buna göre ilk yardımcı, numaralanmış kazazedelerden hangilerine "ağızdan buruna" suni solunum yapmalıdır?`,
    options:[`Yalnız I`,`Yalnız IV`,`II ve III`,`III ve IV`], correct:0 },

  { n:5, section:"İlk Yardım",
    media:{type:"image", file:"/assets/img/sinav-2/soru5.jpeg"},
    caption:`Sırtüstü yatan, burnundan ve kulağından kanama olan, göz çevresinde morluk bulunan yaralı.`,
    stem:`Görseldeki yaralıya ilk yardımcının, hangi uygulamayı yapması uygun değildir?`,
    options:[`Boyun tespiti yapması`,`Yarı oturur pozisyona alması`,`Bilinç durumunu kontrol etmesi`,`Yaşam bulgularını (ABC) değerlendirmesi`], correct:1 },

  { n:6, section:"İlk Yardım",
    stem:`Meydana gelen trafik kazasına tanık olan ilk yardımcı, gerekli güvenlik önlemlerini alarak hemen 112'yi aramıştır. Yaralanan araç sürücüsünün durumunu değerlendirdiğinde; bilincinin kapalı, parmak uçlarında ve dudaklarında solukluk, gözlerinde donukluk, derisinin nemli ve soğuk olduğunu tespit etmiştir.

Bu değerlendirmeye göre, ilk yardımcının yaralı için hangisini yapması doğrudur?`,
    options:[`Ağızdan sıcak içecekler vermesi`,`Başını 30 cm olacak şekilde yukarı kaldırması`,`Vücut sıcaklığını korumak için üzerini örtmesi`,`Hareket ettirmeye çalışması`], correct:2 },

  { n:7, section:"İlk Yardım",
    media:{type:"image", file:"/assets/img/sinav-2/soru7.jpeg"},
    caption:`Kazazede numarası, kırılan kemik (I. üst kol, II. köprücük, III. ön kol) ve uygulanan tespit işlemi görsellerini içeren tablo.`,
    stem:`Tabloda numaralanmış kazazedelerin kırılan kemikleri ve ilk yardımcının uyguladığı tespit işlemleri verilmiştir.

Buna göre uygulanan tespit işlemleri doğru (D), yanlış (Y) olarak değerlendirildiğinde sıralama hangisi olur?`,
    options:[`Y - D - Y`,`Y - D - D`,`D - D - Y`,`D - Y - Y`], correct:2 },

  { n:8, section:"İlk Yardım",
    stem:`İlk yardımcı, kalça veya alt taraf kemiklerinde kırık olan kazazedeye tespit işlemi yaparken hangisine dikkat etmelidir?`,
    options:[`Bacaklar arasına yerleştirilecek destek malzemelerinin sert olmasına`,`Açık kırık oluşmuş ise yaranın temiz bir bezle kapatılmasına`,`Şerit sargıların kırık bölgenin üzerine gelecek şekilde bağlanmasına`,`Yaralının oturur pozisyonda olmasına`], correct:1 },

  { n:9, section:"İlk Yardım",
    stem:`• Ölüm korkusu ve yoğun sıkıntı hissedilir.
• Ağrı şiddetli ve uzun sürelidir, dinlenmekle geçmez.
• Ağrı hissi; sıklıkla kravat bölgesinde görülür, omuzlara, boyuna, çeneye ve sol kola doğru yayılır.

Bu belirtiler, acil bakım gerektiren hastalıklardan hangisiyle ilgilidir?`,
    options:[`Bayılma`,`Kalp krizi`,`Sara krizi`,`Havale`], correct:1 },

  { n:10, section:"İlk Yardım",
    stem:`Hangisi "kısa süreli, yüzeysel ve geçici bilinç kaybı" olarak tanımlanmaktadır?`,
    options:[`Koma`,`Bayılma`,`Epilepsi`,`Kalp spazmı`], correct:1 },

  { n:11, section:"İlk Yardım",
    stem:`Hangisi yaralıyı sedye üzerine yerleştirme yöntemlerinden biri değildir?`,
    optionImages:["/assets/img/sinav-2/soru11a.png","/assets/img/sinav-2/soru11b.png","/assets/img/sinav-2/soru11c.png","/assets/img/sinav-2/soru11d.png"],
    options:[`A`,`B`,`C`,`D`], correct:3 },

  { n:12, section:"İlk Yardım",
    stem:`Yaralı taşımada kullanılan "teskereci yöntemi"nin uygulanış biçimi hangisinde gösterilmiştir?`,
    optionImages:["/assets/img/sinav-2/soru12a.png","/assets/img/sinav-2/soru12b.png","/assets/img/sinav-2/soru12c.png","/assets/img/sinav-2/soru12d.png"],
    options:[`A`,`B`,`C`,`D`], correct:0 },

  { n:13, section:"Trafik ve Çevre",
    stem:`Şehir içinde, yol yapısı veya işaretleme yetersizliği yüzünden trafik kazalarının meydana geldiği yerlerde, yetkililerce teklif edilen tedbirleri almak hangi kurumun görevidir?`,
    options:[`Belediyenin`,`İçişleri Bakanlığının`,`Jandarma Teşkilatının`,`Karayolları Genel Müdürlüğünün`], correct:0 },

  { n:14, section:"Trafik ve Çevre",
    media:{type:"video", file:"/assets/img/sinav-2/soru14.mp4"},
    caption:`[Video] Tehlike uyarı işaretinin bulunduğu yol kesimi.`,
    stem:`I. Direksiyon hakimiyetinde zorlanacağını
II. Kamyonla yan yana geldiğinde rüzgârın şiddetini daha az hissedeceğini
III. İleride trafik kontrolünün olacağını
IV. Yerleşim yeri sınırları içine gireceğini

Sürücü, tehlike uyarı işaretine göre numaralanmış ifadelerden hangilerinin olacağını düşünmelidir?`,
    options:[`I ve II`,`I ve IV`,`I, II ve III`,`II, III ve IV`], correct:0 },

  { n:15, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru15.jpeg"},
    caption:`İki şeritli yolda yan yana giden 1 ve 2 numaralı araçlar ile şerit çizgileri.`,
    stem:`I. Yolun, iki şeritli ve iki yönlü olduğunu
II. 1 numaralı aracın gerektiğinde geçme yapabileceğini
III. 2 numaralı aracın gerektiğinde geçme yapabileceğini

Görseldeki yol çizgileri ve yer işaretlemeleri, numaralanmış ifadelerden hangilerini belirtir?`,
    options:[`I ve II`,`I ve III`,`II ve III`,`I, II ve III`], correct:1 },

  { n:16, section:"Trafik ve Çevre",
    media:{type:"video", file:"/assets/img/sinav-2/soru16.mp4"},
    caption:`[Video] Kavşakta beyaz, sarı ve siyah otomobillerin karşılaşması.`,
    stem:`Videoya göre hangisinin yapılması doğru olur?`,
    options:[`Beyaz otomobil sürücüsünün beklemesi`,`Sarı otomobil sürücüsünün hızlanması`,`Siyah otomobil sürücüsünün sol şeride geçmesi`,`Siyah otomobil sürücüsünün beyaz otomobil sürücüsüne ilk geçiş hakkını vermesi`], correct:0 },

  { n:17, section:"Trafik ve Çevre",
    stem:`Trafik işaretlerinden hangisi, aracın yük taşıma kapasitesine sınırlama getirir?`,
    optionImages:["/assets/img/sinav-2/soru17a.png","/assets/img/sinav-2/soru17b.png","/assets/img/sinav-2/soru17c.png","/assets/img/sinav-2/soru17d.png"],
    options:[`A`,`B`,`C`,`D`], correct:2 },

  { n:18, section:"Trafik ve Çevre",
    media:{type:"video", file:"/assets/img/sinav-2/soru18.mp4"},
    caption:`[Video] Mavi araç sürücüsünün seyri.`,
    stem:`Videoya göre, mavi araç sürücüsünün hangisini ihlal ettiği kesinlikle söylenir?`,
    options:[`Dönüş ve manevra kuralını`,`Geçme kuralını`,`Takip mesafesi kuralını`,`Hız sınırlaması kuralını`], correct:0 },

  { n:19, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru19.jpeg"},
    caption:`Yol çalışması levhalarının bulunduğu bölgede 1 ve 2 numaralı araçlar.`,
    stem:`Görsele göre, hangisinin yapılması doğru olur?`,
    options:[`1 numaralı aracın 2 numaralı araca geçme önceliği vermesi`,`1 numaralı aracın, 2 numaralı araca geçiş kolaylığı sağlamak için, solundaki şeride geçmesi`,`2 numaralı aracın, 1 numaralı araç geçtikten sonra sol şeride geçmesi`,`2 numaralı aracın, 1 numaralı aracı uyararak yavaşlatması`], correct:2 },

  { n:20, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru20.jpeg"},
    caption:`Ortalama hız tespiti levhası altında ilerleyen 1, 2, 3 ve 4 numaralı araçlar.`,
    stem:`Görseldeki yolda, numaralanmış araçlardan hangileri en fazla 70 km/saat hızla yollarına devam edebilir?`,
    options:[`Yalnız 4`,`1 ve 2`,`2 ve 3`,`3 ve 4`], correct:1 },

  { n:21, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru21.jpeg"},
    caption:`Dağ yolunda virajlı kesimde ilerleyen 1 numaralı beyaz araç.`,
    stem:`I. Takip mesafesini artırması
II. Hızını azaltması
III. Bulunduğu şeridin soluna yanaşması

Görsele göre, 1 numaralı araç sürücüsünün numaralanmış davranışlardan hangilerini yapması trafik kazası riskini azaltır?`,
    options:[`I ve II`,`I ve III`,`II ve III`,`I, II ve III`], correct:0 },

  { n:22, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru22.jpeg"},
    caption:`Şehirlerarası yolda geçme yapan 1, 2, 3 ve 4 numaralı araçlar ile şerit sayısını gösteren mavi levha.`,
    stem:`Görsele göre, numaralı araçlardan hangileri hatalı geçme yapmaktadır?`,
    options:[`Yalnız 2`,`Yalnız 3`,`2 ve 3`,`1, 2 ve 3`], correct:1 },

  { n:23, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru23.jpeg"},
    caption:`Bölünmüş yolda ayrım noktasına yaklaşan otomobil ve kamyon.`,
    stem:`Görsele göre, Adana istikametine gitmek isteyen otomobil sürücüsü hakkında hangisi söylenemez?`,
    options:[`Araç ışıklarını doğru yerde kullanmadığı`,`Dönüş öncesi doğru şeride girmediği`,`Kamyon sürücüsünü zor durumda bıraktığı`,`Geçme kurallarına uymadığı`], correct:0 },

  { n:24, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru24.jpeg"},
    caption:`Kavşakta 1, 2 ve 3 numaralı üç aracın konumunu gösteren kroki.`,
    stem:`Görseldeki kavşakta ilk geçiş hakkı sıralaması nasıl olmalıdır?`,
    options:[`1 - 2 - 3`,`1 - 3 - 2`,`2 - 1 - 3`,`3 - 2 - 1`], correct:1 },

  { n:25, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru25.jpeg"},
    caption:`Dar köprüde karşılaşan 1 numaralı otomobil ile 2 numaralı kamyon.`,
    stem:`Görseldeki gibi bir karşılaşmada, 2 numaralı araç sürücüsü ne yapmalıdır?`,
    options:[`Geçiş önceliğini kendisi kullanmalı`,`Hızlanıp köprüye 1 numaralı araçtan önce girmeli`,`Geçiş önceliğini 1 numaralı araca vermeli`,`1 numaralı aracın daralan yol bölümüne girmemesi için selektör yaparak uyarmalı`], correct:2 },

  { n:26, section:"Trafik ve Çevre",
    stem:`Geçiş üstünlüğüne sahip araçların, duyulan uyarı işaretini aldığımızda, ilk önce yapmamız gereken hangisidir?`,
    options:[`Derhal sağ şeride yanaşmak`,`Sesin yönünü tayin etmek`,`Kavşakta bulunuyorsak, kavşağı hemen boşaltmak`,`Önümüzdeki araçları, hızlanmaları için uyarmak`], correct:1 },

  { n:27, section:"Trafik ve Çevre",
    stem:`"İşaret levhalarına yaklaşım yönünde ve park izni verilen yerler dışında; yerleşim birimleri içinde - - - - metre ve yerleşim birimleri dışında - - - - metre mesafede duraklamak yasaktır."

Bu cümlede boş bırakılan yerlere hangileri getirilmelidir?`,
    options:[`15 - 100`,`20 - 150`,`30 - 200`,`40 - 250`], correct:0 },

  { n:28, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru28.jpeg"},
    caption:`Keskin virajlı dağ yolunda ilerleyen otomobil ve viraj oklu levha.`,
    stem:`I. Hızlarını artırmaları
II. Virajı geniş bir kavisle almaları
III. Öndeki aracı geçmeleri

Görseldeki gibi bir kara yolu bölümünde seyreden sürücülerin, numaralanmış davranışlardan hangilerini yapmaları tehlikeli durumların oluşmasına neden olur?`,
    options:[`I ve II`,`I ve III`,`II ve III`,`I, II ve III`], correct:1 },

  { n:29, section:"Trafik ve Çevre",
    stem:`I. Yeteri kadar aydınlatılmış yollara girdiğimizde
II. Yayalarla aynı yönde ilerliyorsak
III. Demiryolu geçidine geldiğimizde
IV. Geceleyin önümüzdeki aracı geçeceğimiz zaman

Uzun hüzmeli far açıkken, numaralanmış durumlardan hangileri olursa kısa hüzmeli farı kullanmalıyız?`,
    options:[`I ve II`,`I ve IV`,`II ve III`,`I, III ve IV`], correct:1 },

  { n:30, section:"Trafik ve Çevre",
    media:{type:"image", file:"/assets/img/sinav-2/soru30.jpeg"},
    caption:`Otoyol bilgi levhası.`,
    stem:`Görseldeki otoyol bilgi levhası hangisini bildirir?`,
    options:[`Cep telefonu sinyalinin güçlü olduğunu`,`Radyo yayınlarının yol boyunca dinlenebileceğini`,`Ücretli otoyola girileceğini`,`Yol boyunca elektronik denetleme sisteminin olduğunu`], correct:2 },

  { n:31, section:"Trafik ve Çevre",
    stem:`Hangisi trafik kaza oranını etkileyen etmenlerden biri değildir?`,
    options:[`Aracın yük durumu`,`Kural ihlalleri`,`Araç bakımları`,`Aracın beygir gücü`], correct:3 },

  { n:32, section:"Trafik ve Çevre",
    media:{type:"video", file:"/assets/img/sinav-2/soru32.mp4"},
    caption:`[Video] Trafikte oluşan tehlikeli durum.`,
    stem:`Videodaki tehlikeli durum, sürücülerin hangi kuralı ihlal etmeleri sonucunda oluşmuştur?`,
    options:[`Takip mesafesi kuralını`,`Geçme kuralını`,`Kavşaklarda ilk geçiş hakkı kuralını`,`Şerit takip kuralını`], correct:3 },

  { n:33, section:"Trafik ve Çevre",
    stem:`I. Rot başlarının boşluk yapması
II. Ön cam sileceklerinin çalışmaması
III. Park lambalarının yanmaması
IV. Kısa hüzmeli far ayarının bozuk olması

Araç muayenesi sırasında, numaralanmış arızalardan hangileri ağır kusur olarak değerlendirilir?`,
    options:[`I ve IV`,`II ve IV`,`I, II ve III`,`II, III ve IV`], correct:2 },

  { n:34, section:"Trafik ve Çevre",
    stem:`Hangisi aracın durma mesafesini etkileyen faktörlerden biri değildir?`,
    options:[`Kaplamanın cinsi`,`Yolun eğimi`,`Aracın hızı`,`Hidrolik direksiyon`], correct:3 },

  { n:35, section:"Trafik ve Çevre",
    stem:`Hangisini yapmak çevrenin temiz kalmasına katkı sağlar?`,
    options:[`Gereksiz yere korna çalmak`,`Seyahat esnasında, yiyecek atıklarını otoyol kenarlarına bırakmak`,`Egzoz emisyon ölçümünü geciktirmek`,`Araç bakımlarını zamanında yaptırmak`], correct:3 },

  { n:36, section:"Trafik ve Çevre",
    stem:`"Geceleyin şehirlerarası kara yolunda seyrederken araçla karşılaşıldığında kısa farları kullanmak gerekir. Bu durumda, net görüş mesafesi ortalama 25 metreye düşer."

Bu bilgiye göre, kısa farların kullanılması gerektiğinde hangisini yapmak doğru olur?`,
    options:[`Karşı taraf ikazda bulunmazsa uzun farla devam etmek`,`Araç hızını, herhangi bir tehlike anında, kolayca durulabilecek hıza getirmek`,`Yolu daha iyi görmek için art arda kısa aralıklarla selektör yapmak`,`Yolun sağından bir tehlike gelebileceği düşünülerek iyice sola yanaşmak`], correct:1 },

  { n:37, section:"Araç Tekniği",
    stem:`Hangisi, motor soğutma sisteminin elemanı değildir?`,
    options:[`Balata`,`Su pompası`,`Radyatör`,`Termostat`], correct:0 },

  { n:38, section:"Araç Tekniği",
    stem:`Aşağıda motor yağı kontrol edilirken yapılması gereken işlemler karışık verilmiştir.
I. Motor yağ seviye çubuğu çekilip temizlenmeli
II. Motor yağ çubuğu tekrar yerine daldırılıp çekilip kontrol edilmeli
III. Araç düz bir zeminde durdurulup motor kaputu açılmalı
IV. Yağ miktarının max-min seviyesi arasında olduğu görülmeli

İşlemlerin doğru sıralanışı hangisidir?`,
    options:[`I, II, III ve IV`,`II, I, IV ve III`,`III, I, IV ve II`,`III, I, II ve IV`], correct:3 },

  { n:39, section:"Araç Tekniği",
    media:{type:"image", file:"/assets/img/sinav-2/soru39.jpeg"}, mediaWidth:"200px",
    caption:`Lastik basıncı ikaz ışığı sembolü.`,
    stem:`Görseldeki ikaz ışığı hangi durumda yanmaz?`,
    options:[`Lastik basıncı azaldığında`,`Lastik ısındığında`,`Lastik patladığında`,`Sensör arızalandığında`], correct:1 },

  { n:40, section:"Araç Tekniği",
    stem:`Hangisi, servis veya tamir atölyeleri tarafından yapılmalıdır?`,
    options:[`Silecek lastiklerinin kontrolü`,`Antifiriz yoğunluk derecesi kontrolü`,`Lastik hava basınç kontrolü`,`Motor yağı seviyesinin kontrolü`], correct:1 },

  { n:41, section:"Araç Tekniği",
    stem:`Hangi parçanın düzgün çalışmaması, şarj ikaz lambasının yanmasına sebep olur?`,
    options:[`V kayışının`,`Triger kayışının`,`Marş motorunun`,`Radyatörün`], correct:0 },

  { n:42, section:"Araç Tekniği",
    media:{type:"video", file:"/assets/img/sinav-2/soru42.mp4"},
    caption:`[Video] Seyir hâlindeki araçta oluşan durum.`,
    stem:`Videoya göre sürücü nasıl davranmalıdır?`,
    options:[`Sabit hızla aynı şeritte yoluna devam etmeli`,`Sol şeride geçip derhal servise gitmeli`,`Yavaşlayıp sağ şeritten yoluna devam etmeli`,`Trafik kurallarına uygun olarak derhal durmalı`], correct:3 },

  { n:43, section:"Araç Tekniği",
    stem:`Hangisi, motorun hararet yapmasına sebep olan durumlardan biri değildir?`,
    options:[`Termostatın arızalanması`,`Devirdaim hortumunun yırtılması`,`Antifriz seviyesinin düşük olması`,`Vantilatör kayışının gevşemesi`], correct:2 },

  { n:44, section:"Araç Tekniği",
    stem:`I. Mümkün olduğunca az fren yapmak
II. Vitese göre daha düşük devirde araç kullanmak
III. Araç ilk çalıştırıldığında motora tam güç vermek
IV. Vitese göre yüksek devirde araç kullanmak

Numaralanmış ifadelerden hangilerinin yapılması, yakıt tüketiminin artmasına sebep olur?`,
    options:[`I ve II`,`I ve IV`,`I, II ve III`,`II, III ve IV`], correct:3 },

  { n:45, section:"Trafik Adabı",
    stem:`Hangisi, toplum adabına aykırı davranışlardandır?`,
    options:[`Trafikte aracı arızalanan birine yardımcı olmak`,`Kaza, deprem, sel gibi felaketlerden çıkar sağlamaya çalışmak`,`Engellilere ayrılmış alanların dışına park etmek`,`Toplu taşıma araçlarındaki yaşlı, çocuklu veya engelli insanlara yer vermek`], correct:1 },

  { n:46, section:"Trafik Adabı",
    stem:`Deprem, sel gibi doğal afetlerden etkilenenlere yardım götürmeye çalışan araçlara kolaylık sağlayan sürücünün hangisine önem verdiği söylenemez?`,
    options:[`Feragata`,`Diğerkâmlığa`,`Empatiye`,`Aceleciliğe`], correct:3 },

  { n:47, section:"Trafik Adabı",
    media:{type:"image", file:"/assets/img/sinav-2/soru47.jpeg"},
    caption:`Kaldırım üzerine, görme engelliler için ayrılmış hissedilebilir yüzeyin üstüne park etmiş araç.`,
    stem:`Görseldeki park etmiş aracın sürücüsüyle ilgili hangisi kesinlikle söylenir?`,
    options:[`Trafik adabına uygun davrandığı`,`Empati kurabilen biri olduğu`,`Trafikte saygı kavramına önem verdiği`,`Sorumluluk bilincinin zayıf olduğu`], correct:3 },

  { n:48, section:"Trafik Adabı",
    stem:`I. Kaygıları artar.
II. Kalp atışları hızlanır.
III. Saldırgan tutum sergilemezler.

Trafikte yaşanan stresin, bireyler üzerindeki etkileriyle ilgili numaralanmış ifadeler doğru (D), yanlış (Y) olarak değerlendirildiğinde sıralama hangisi olur?`,
    options:[`D - D - Y`,`D - Y - D`,`D - D - D`,`Y - D - D`], correct:0 },

  { n:49, section:"Trafik Adabı",
    media:{type:"image", file:"/assets/img/sinav-2/soru49.jpeg"},
    caption:`Sürücü bakış açısından, karşıya geçmeye çalışan yaya.`,
    stem:`Görselde karşıya geçmeye çalışan yayanın hızlı hareket etmesi için el, kol ve sözle uyarılarda bulunan sürücüyle ilgili hangisi söylenir?`,
    options:[`İletişim kabiliyetinin yüksek olduğu`,`Empati kurabildiği`,`Sabırlı hareket edemediği`,`Saygı kavramına önem verdiği`], correct:2 },

  { n:50, section:"Trafik Adabı",
    media:{type:"image", file:"/assets/img/sinav-2/soru50.jpeg"},
    caption:`Egzozundan yoğun duman çıkaran araç.`,
    stem:`Görseldeki gibi emisyon değeri yüksek egzoz dumanı çıkaran araçların kullanılması, hak ihlallerinden hangisinin kapsamına girmez?`,
    options:[`Doğa ve Çevreye Karşı Yapılan Hak İhlalleri`,`Kamu Hak İhlalleri`,`Diğer Canlılara Karşı Yapılan Hak İhlalleri`,`Bireylere Karşı Yapılan Hak İhlalleri`], correct:1 }
];
