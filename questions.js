// MTSK E-Sınav — Sınav 1 (50 soru). Cevaplar: correct 0=A,1=B,2=C,3=D
// media.file yoksa/klasörde bulunamazsa caption (açıklama) gösterilir; dosya eklenince otomatik görünür.
window.QUESTIONS = [
  { n:1, section:"İlk Yardım",
    stem:`I. Ambulans ekiplerince müdahale yapılması
II. Olay yerinde, ilk yardımcı tarafından temel yaşam desteği yapılması
III. Hastane acil servislerinde müdahale yapılması
IV. Sağlık kuruluşuna haber verilmesi

Hayat kurtarma zinciri halkalarının doğru sıralaması hangisinde verilmiştir?`,
    options:[`I - III - II - IV`,`II - III - I - IV`,`III - II - IV - I`,`IV - II - I - III`], correct:3 },

  { n:2, section:"İlk Yardım",
    stem:`Yetişkinlerde temel yaşam desteği ile ilgili uygulamalardan hangisi doğrudur?`,
    options:[`Göğüs kemiği 3 cm aşağı inecek şekilde bası yapılması`,`Temel yaşam desteğine yapay solunum ile başlanması`,`30 kalp masajı, 2 yapay solunum şeklinde uygulanması`,`Kalp masajı hızının dakikada 30 bası olacak şekilde ayarlanması`], correct:2 },

  { n:3, section:"İlk Yardım",
    media:{type:"image", file:"images/soru3.png"}, mediaWidth:"174px",
    caption:`Solunumu olmayan bebeğe kalp basısı için pozisyon verilmiş; göğüste I, II, III, IV bölgeleri işaretli (meme başı hattı kesikli çizgi).`,
    stem:`Trafik kazası sonucu araç dışına fırlayan bir bebeğin solunumunun olmadığını tespit eden ilk yardımcı, 2 kurtarıcı solunum verdikten sonra kalp basısı uygulamak için bebeğe pozisyon vermiştir.

İlk yardımcı, bir elinin orta ve yüzük parmağını hangi bölgeye yerleştirmelidir?`,
    options:[`I`,`II`,`III`,`IV`], correct:2 },

  { n:4, section:"İlk Yardım",
    stem:`• Bir el alna, diğer elin iki parmağı çene kemiğinin üzerine yerleştirilir.
• Alından bastırılıp çeneden kaldırılarak baş geriye doğru itilir.

Uygulama basamakları verilen ve kazazedenin hava yolunu açmak için kullanılan pozisyon hangisidir?`,
    options:[`Şok`,`Yarı oturuş`,`Baş geri-çene yukarı`,`Yarı yüzükoyun-yan yatış`], correct:2 },

  { n:5, section:"İlk Yardım",
    media:{type:"image", file:"images/soru5.png"},
    caption:`Elde/bilekte fışkırır tarzda (atardamar) kanama görseli.`,
    stem:`Görseldeki kanama türünde yaralıya ilk yardım olarak hangisinin yapılması yanlıştır?`,
    options:[`Kanayan bölgeyi yukarı kaldırmak`,`Kanayan yer üzerine temiz bir bez koyarak baskı uygulamak`,`Kanayan yere en uzak olan basınç noktasına elle baskı uygulamak`,`Yara üzerindeki bez kaldırılmadan bandaj ile sararak baskı uygulamak`], correct:2 },

  { n:6, section:"İlk Yardım",
    media:{type:"image", file:"images/soru6.png"},
    caption:`Her iki omuz üzerinden çapraz (sırt çantası askısı benzeri) tespit yöntemi görseli.`,
    stem:`Görseldeki tespit yöntemi hangi kemiğin kırılması durumunda uygulanır?`,
    options:[`Pazı`,`Boyun`,`Omuz`,`Köprücük`], correct:3 },

  { n:7, section:"İlk Yardım",
    stem:`Açık kırıkla ilgili hangisi söylenemez?`,
    options:[`Kan kaybı olur.`,`Deri bütünlüğü bozulmaz.`,`Enfeksiyon tehlikesi yüksektir.`,`Kemik bütünlüğü bozulur.`], correct:1 },

  { n:8, section:"İlk Yardım",
    media:{type:"image", file:"images/soru8.png"},
    caption:`Yerde yan yatış (koma) pozisyonu verilmiş kazazede görseli.`,
    stem:`Görseldeki pozisyon hangi durumdaki yaralıya uygulanır?`,
    options:[`Bilinci kapalı, solunum ve nabzı olan`,`Bacak bölgesinde deri ve kemik bütünlüğü bozulmuş olan`,`Karın bölgesinde delici cisim bulunan`,`Kulak ve burun kanaması olan`], correct:0 },

  { n:9, section:"İlk Yardım",
    stem:`I. Vücudu sıkan giysiler gevşetilir.
II. Sırtüstü yatırılarak ayakları 45 cm kaldırılır.
III. Kusma varsa mide içeriğini yutmaması için yarı oturur pozisyonda tutulur.
IV. Solunum yolu açıklığı kontrol edilir ve açıklığın korunması sağlanır.

Numaralanmış ifadelerden hangileri bayılmış olan kazazedeye yapılması gereken ilk yardım uygulamalarındandır?`,
    options:[`I ve IV`,`II ve III`,`I, III ve IV`,`I, II, III ve IV`], correct:0 },

  { n:10, section:"İlk Yardım",
    stem:`Kaza yapmış bir aracı gören ilk yardımcı, kendisinin ve çevrenin güvenliğini sağladıktan sonra araç sürücüsünün bilincinin kapalı, solunumunun olmadığını ve kazazedenin ayaklarının pedala sıkışmamış olduğunu tespit etmiştir.

Buna göre, ilk yardımcının kazazedeyi araç içerisinden çıkarırken uygulaması gereken doğru teknik hangisidir? (Rentek manevrası)`,
    optionImages:["images/soru10a.png","images/soru10b.png","images/soru10c.png","images/soru10d.png"],
    options:[`A`,`B`,`C`,`D`], correct:1 },

  { n:11, section:"İlk Yardım",
    stem:`Bir kazazedenin taşınmasında, uyulması gereken genel kurallardan hangisi doğrudur?`,
    options:[`Kazazedenin baş-boyun-gövde ekseni esas alınarak en az 6 destek noktasından kavranması`,`Kazazedenin mümkün olduğunca çok hareket ettirilmesi`,`İlk yardımcının kalkarken ağırlığını karın kaslarına vermesi`,`İlk yardımcının kendi sağlığını riske atması`], correct:0 },

  { n:12, section:"Trafik ve Çevre",
    stem:`Trafik kurallarına uymama eğiliminde olan bir sürücünün hangi davranışı gösterme olasılığı yüksektir?`,
    options:[`Hız sınırına uyma`,`Yayaya yol verme`,`Trafik levhalarını fark etme`,`Sürekli şerit değiştirerek araç kullanma`], correct:3 },

  { n:13, section:"Trafik ve Çevre",
    stem:`Yapım ve bakımından sorumlu olduğu kara yollarında, İçişleri Bakanlığının uygun görüşü alınmak suretiyle, Kara Yolları Trafik Yönetmeliği'nde belirlenen hız sınırlarının üstünde veya altında hız sınırları belirlemek ve işaretlemek hangi kurumun görev ve yetkisidir?`,
    options:[`Sağlık Bakanlığının`,`Emniyet Genel Müdürlüğünün`,`Kara Yolları Genel Müdürlüğünün`,`Millî Eğitim Bakanlığının`], correct:2 },

  { n:14, section:"Trafik ve Çevre",
    stem:`Aralıklı yanıp sönen kırmızı ışık, trafik işaretlerinden hangisi ile aynı anlamdadır?`,
    optionImages:["images/soru14a.png","images/soru14b.png","images/soru14c.png","images/soru14d.png"],
    options:[`A`,`B`,`C`,`D`], correct:0,
    note:`Yanıp sönen kırmızı ışık = DUR levhası (A) ile aynı anlamdadır.` },

  { n:15, section:"Trafik ve Çevre",
    media:{type:"image", file:"images/soru15.png"},
    caption:`İki şeritli yolda sol şeritte ilerleyen mavi araç; sağda "şerit azalması" (sol şerit bitip sağa katılıyor) levhası.`,
    stem:`Görseldeki mavi renkli aracın sürücüsü nasıl davranmalıdır?`,
    options:[`En sol şeride geçmeli`,`Yavaşlayarak sağ şeride girmeli`,`Hızlanarak bulunduğu şeritte devam etmeli`,`Kırmızı renkli aracı uyararak yavaşlamasını sağlamalı`], correct:1 },

  { n:16, section:"Trafik ve Çevre",
    stem:`Hangisi "köprü yaklaşımı" levhasıdır?`,
    optionImages:["images/soru16a.png","images/soru16b.png","images/soru16c.png","images/soru16d.png"],
    options:[`A`,`B`,`C`,`D`], correct:3 },

  { n:17, section:"Trafik ve Çevre",
    media:{type:"image", file:"images/soru17.png"},
    caption:`Sürücü bakış açısı; yol kenarında bir trafik levhası (kasis / tümsek).`,
    stem:`I. Yükün hasar görmesi
II. Direksiyon hâkimiyetinin kaybolması
III. Araç aksının kırılması veya amortisörlerin arızalanması

Görseldeki sürücü trafik işaretini fark etmeden yoluna devam ederse numaralanmış ifadelerden hangilerinin olma ihtimali vardır?`,
    options:[`I ve II`,`I ve III`,`II ve III`,`I, II ve III`], correct:3 },

  { n:18, section:"Trafik ve Çevre",
    stem:`Sürücünün hangisini yapması kural ihlali sayılır?`,
    options:[`Üç şeritli ve iki yönlü yollarda sağ şeritten gitmesi`,`Aracın cinsine ve hızına uygun olan şeridi kullanması`,`Geçme, dönme gibi mecburi hâller dışında şerit değiştirmesi`,`Şerit değiştirmeden önce, gireceği şeritteki araçların güvenle geçişlerini beklemesi`], correct:2 },

  { n:19, section:"Trafik ve Çevre",
    media:{type:"image", file:"images/soru19.png"},
    caption:`Kırmızı araç önündeki mavi aracın arkasında; karşı yönden araç gelmekte.`,
    stem:`Görseldeki kırmızı renkli aracın sürücüsü nasıl davranmalıdır?`,
    options:[`Sol şeride geçip beklemeli`,`Önündeki aracın geçişini beklemeli`,`Önündeki aracı acele etmesi için uyarmalı`,`Sol şeride geçip yoluna devam etmeli`], correct:1 },

  { n:20, section:"Trafik ve Çevre",
    stem:`Trafik kuralının ihlal edildiği tarihten geriye doğru bir yıl içinde, toplam 100 ceza puanını ilk defa aştığı tespit edilen sürücülerin sürücü belgesi kaç ay süre ile geri alınır?`,
    options:[`2`,`3`,`6`,`12`], correct:0 },

  { n:21, section:"Trafik ve Çevre",
    media:{type:"video", file:"images/soru21.mp4"},
    caption:`[Video] Motosiklet sürücüsünün trafikte geçiş/manevra yaptığı sahne.`,
    stem:`I. Can ve mal güvenliğini tehlikeye attığı
II. İleri sürüş tekniklerine sahip olduğu
III. Şerit takip kurallarına uyduğu
IV. Geçme kurallarına uymadığı

Motosiklet sürücüsü için numaralanmış ifadelerden hangileri kesinlikle söylenebilir?`,
    options:[`I ve II`,`I ve IV`,`II ve III`,`III ve IV`], correct:1 },

  { n:22, section:"Trafik ve Çevre",
    stem:`Arkadan çarpma sonucunda meydana gelen trafik kazalarının en önemli sebebi hangisidir?`,
    options:[`Takip mesafesi kuralına uyulmaması`,`Görüş mesafesinin kötü olması`,`Öndeki aracın durması`,`Havanın yağışlı olması`], correct:0 },

  { n:23, section:"Trafik ve Çevre",
    media:{type:"video", file:"images/soru23.mp4"},
    caption:`[Video] Sisli/yağmurlu yolda seyir.`,
    stem:`Videodaki kazayla ilgili hangisi kesinlikle söylenir?`,
    options:[`Yeşil araç sürücüsünün ani fren yapması kazaya sebep olmuştur.`,`Mavi araç sürücüsünün hatalı geçme yapması kazaya sebep olmuştur.`,`Araç sürücüleri takip mesafesine uymaktadır.`,`Kaza, iklim şartlarına bağlı olarak meydana gelmiştir.`], correct:1 },

  { n:24, section:"Trafik ve Çevre",
    media:{type:"image", file:"images/soru24.png"},
    caption:`İki yönlü ve üç şeritli yolda seyreden 1, 2, 3 numaralı araçlar. Orta şerit sollama içindir.`,
    stem:`Görselde iki yönlü ve üç şeritli kara yolu bölümünde seyreden araçlar verilmiştir.

Yol çizgilerine göre hangi numaralı araç sürücüleri hatalı sollama yapmaktadır?`,
    options:[`1 ve 2`,`1 ve 3`,`2 ve 3`,`1, 2 ve 3`], correct:0 },

  { n:25, section:"Trafik ve Çevre",
    media:{type:"video", file:"images/soru25.mp4"},
    caption:`[Video] Beyaz otomobilin seyri.`,
    stem:`Videoya göre, beyaz otomobilin sürücüsü için hangisi kesinlikle söylenir?`,
    options:[`Uyuşturucu veya uyarıcı madde etkisinde araç kullandığı`,`Uykusuz ve yorgun olarak araç kullandığı`,`Şerit takip ve manevra kurallarına uymadığı`,`İleri sürüş tekniklerine uygun araç kullandığı`], correct:2 },

  { n:26, section:"Trafik ve Çevre",
    media:{type:"video", file:"images/soru26.mp4"},
    caption:`[Video] Karavan/römork çekilen yolda seyir.`,
    stem:`Videoya göre, sürücü nasıl bir tehlikenin olabileceğini düşünmelidir?`,
    options:[`Rüzgar nedeniyle direksiyon hakimiyetini kaybedebileceğini`,`Orta şeritteki otomobilin ani fren yapabileceğini`,`Bir aracın benzin istasyonundan yola çıkabileceğini`,`Yolun ilerisinde trafik denetimi yapılabileceğini`], correct:2 },

  { n:27, section:"Trafik ve Çevre",
    stem:`I. Güvenlik güçlerine ait araçlar
II. Organ ve doku nakli yapan araçlar
III. İtfaiye araçları ile benzeri acil müdahale araçları
IV. Ambulans ve özel amaçlı taşıtlarla yaralı ve acil hasta taşıyan diğer araçlar

Verilen araçların geçiş üstünlüğünü kullanmadaki doğru sıralaması hangisidir?`,
    options:[`II - III - IV - I`,`III - IV - I - II`,`IV - III - I - II`,`IV - II - III - I`], correct:3 },

  { n:28, section:"Trafik ve Çevre",
    stem:`Araç sürücülerinin duraklanan veya park edilen yerden çıkarken;
I. ışıkla veya kolla çıkış işareti vermeleri,
II. araçlarını ve araçların etrafını kontrol etmeleri,
III. yoldan geçen araçları ikaz ederek durdurmaları,
IV. görüş alanları dışında kalan yerler varsa gözcü bulundurmaları mecburidir.

Numaralanmış bilgilerden hangileri doğrudur?`,
    options:[`I ve III`,`I, II ve IV`,`II, III ve IV`,`I, II, III ve IV`], correct:1 },

  { n:29, section:"Trafik ve Çevre",
    stem:`• Trafik işaretiyle yasaklanmış olan yerlerde
• Belirlenmiş yangın musluklarına her iki yönden 5 metre mesafe içinde
• Yerleşim yeri içinde kavşaklara ve bağlantı yollarına 5 metre mesafe içinde

Verilen yerlerde hangisi yasaktır?`,
    options:[`Durmak`,`Duraklamak`,`Hızı azaltmak`,`Vites yükseltmek`], correct:1 },

  { n:30, section:"Trafik ve Çevre",
    stem:`I. Yolcuların koruyucu tertibat kullanması
II. Kasanın yan ve arka kapaklarının kapalı olması
III. Yüklerin sağlam olarak yerleştirilmiş ve bağlanmış olması

Kamyon, kamyonet ve römorklarda yükle birlikte yolcu taşınırken numaralanmış ifadelerden hangilerinin yapılması zorunludur?`,
    options:[`Yalnız I`,`I ve II`,`II ve III`,`I, II ve III`], correct:2 },

  { n:31, section:"Trafik ve Çevre",
    stem:`Araçlarda emniyet kemeri kullanımının zorunlu olması ile hangisi hedeflenmektedir?`,
    options:[`Kazaların önlenmesi`,`Sürücülerin dikkatinin artırılması`,`Denetimlerde herhangi bir sorun yaşanmaması`,`Kaza anında ölüm ve yaralanmaların en aza indirilmesi`], correct:3 },

  { n:32, section:"Trafik ve Çevre",
    stem:`Ölümle sonuçlanan trafik kazalarına asli kusurlu olarak sebebiyet veren sürücülerin sürücü belgeleri, ilgili mahkeme tarafından kaç yıl süre ile geri alınır?`,
    options:[`1`,`2`,`3`,`4`], correct:0 },

  { n:33, section:"Araç Tekniği",
    stem:`Muayene süresi dolmasa bile aracın özel teknik muayenesi hangi durumda zorunludur?`,
    options:[`Araç sahibinin değişmesi`,`Maddi hasarlı kazaya karışması`,`Trafik zabıtalarının gerekli görmesi`,`Aracın periyodik bakımının yapılmaması`], correct:2 },

  { n:34, section:"Trafik ve Çevre",
    stem:`Sürüş güvenliğini hangisi olumsuz yönde etkiler?`,
    options:[`Viraja girmeden önce hızı artırmak`,`Aracı kullanırken yola konsantre olmak`,`Yüksek hızlarda ani manevra yapmaktan kaçınmak`,`Hız ile fren mesafesi arasındaki ilişkiyi öğrenmek`], correct:0 },

  { n:35, section:"Trafik ve Çevre",
    stem:`Hangisi atıkların çevreye verdiği zararlardan biri değildir?`,
    options:[`Kötü koku yayması`,`Çirkin görünüm arz etmesi`,`Hastalık bulaştıran zararlıların üremesine sebep olması`,`Toplanıp işlenerek tekrar kullanılabilir hâle getirilmesi`], correct:3 },

  { n:36, section:"Araç Tekniği",
    stem:`Motor parçalarından hangisinin işlevini kaybetmesi durumunda motorun içine su sızar?`,
    optionImages:["images/soru36a.png","images/soru36b.png","images/soru36c.png","images/soru36d.png"],
    options:[`A`,`B`,`C`,`D`], correct:0,
    note:`Doğru: A = silindir kapak contası. (B krank mili, C buji, D piston/kol.)` },

  { n:37, section:"Araç Tekniği",
    media:{type:"image", file:"images/soru37.png"},
    caption:`Gösterge panelinde ABS uyarı ışığı sembolü.`,
    stem:`Şekildeki uyarı ışığının araç gösterge panelinde yanması aracın hangi sisteminde arıza olduğunu belirtir?`,
    options:[`Marş`,`Şarj`,`Ateşleme`,`Fren`], correct:3 },

  { n:38, section:"Araç Tekniği",
    media:{type:"image", file:"images/soru38.jpeg"},
    caption:`Gösterge panelinde cam yıkama suyu (silecek suyu) uyarı sembolü.`,
    stem:`Şekildeki uyarı ışığı araç gösterge panelinde yandığında sürücü ne yapmalıdır?`,
    options:[`Aracı durdurup motoru stop etmeli`,`Araç motoruna yağ ilave etmeli`,`Silecek suyu deposuna su eklemeli`,`Motor soğutma suyu seviyesini kontrol etmeli`], correct:2 },

  { n:39, section:"Araç Tekniği",
    stem:`Sürüşe başlamadan önce koltuk ve ayna ayarlarının yapılmasının sebebi hangisidir?`,
    options:[`Sürüş konforu ve güvenliğini sağlamak`,`Aracın ivmelenme süresini artırmak`,`Koltukların yıpranmasını engellemek`,`Yakıt tüketimini azaltmak`], correct:0 },

  { n:40, section:"Araç Tekniği",
    stem:`I. Akü şarjının azalması
II. Fren balatalarının azalması
III. Motor yağının özelliğini kaybetmesi

Aracın çok uzun süre kullanılmaması durumunda numaralanmış ifadelerden hangileri meydana gelebilir?`,
    options:[`Yalnız III`,`I ve II`,`I ve III`,`I, II ve III`], correct:2 },

  { n:41, section:"Araç Tekniği",
    stem:`Dizel yakıt kullanan bir araca yanlışlıkla benzin konulması durumunda hangisinin yapılması uygundur?`,
    options:[`Aracın düşük hızda sürülmesi`,`Yakıt deposunun boşaltılması`,`Aracın yüksek devirde kullanılması`,`Hava filtresinin değiştirilmesi`], correct:1 },

  { n:42, section:"Araç Tekniği",
    stem:`I. Şarj
II. ABS
III. Yağ basıncı

Numaralanmış ikaz lambalarından hangilerinin araç gösterge panelinde yanması, aracın kurallara uygun olarak derhal durdurulmasını ve kontağın kapatılmasını gerektirir?`,
    options:[`Yalnız I`,`I ve II`,`I ve III`,`II ve III`], correct:2 },

  { n:43, section:"Araç Tekniği",
    stem:`Aracın motoru yağlama yapmadığında gösterge panelinde hangi lamba yanar?`,
    optionImages:["images/soru43a.png","images/soru43b.png","images/soru43c.png","images/soru43d.png"],
    options:[`A`,`B`,`C`,`D`], correct:3,
    note:`Doğru: D = yağ lambası (kırmızı yağdanlık). (A yakıt, B servis/anahtar, C motor arıza.)` },

  { n:44, section:"Araç Tekniği",
    stem:`• Ani duruş ve hızlanmalardan kaçınılması
• Tavsiye edilen tip ve ebatlarda araç lastiği kullanılması
• Araçta yapılması gerekli bakım ve ayarların zamanında yapılması

Verilenlerin yapılması durumunda hangisinin gerçekleşmesi beklenir?`,
    options:[`Çevre kirliliğinin artması`,`Sürüş konforunun azalması`,`Trafik yoğunluğunun artması`,`Aracın daha az yakıt tüketmesi`], correct:3 },

  { n:45, section:"Trafik Adabı",
    stem:`I. Trafikteki bütün kuralların nedenini öğrenir.
II. Araç kullanırken yapacağı bir kural ihlalinin sonucunda sadece maddi ceza olduğunu düşünür.
III. Trafik içinde yapacağı bir kural ihlalinde, kendisinin ya da sevdiklerinin canını tehlikeye attığının farkındadır.

Numaralanmış ifadelerden hangileri trafik adabına sahip olan bir sürücü için söylenebilir?`,
    options:[`I ve II`,`I ve III`,`II ve III`,`I, II ve III`], correct:1 },

  { n:46, section:"Trafik Adabı",
    stem:`Sürücünün trafik ortamında yaptığı davranışlardan hangisi, diğer sürücülerin dikkatinin dağılmasına ya da paniğe kapılmalarına sebep olabilir?`,
    options:[`Davranışlarının sonuçlarını düşünerek hareket etmesi`,`Sürekli ve ani şerit değiştirerek araç kullanması`,`Aracını kullanırken trafik kurallarının bilincinde olması`,`Trafik içindeki davranışlarının sorumluluğunu üstlenerek araç kullanması`], correct:1 },

  { n:47, section:"Trafik Adabı",
    stem:`Bir araç sürücüsünün kendini geçmekte olan bir araca yavaşlayarak kolaylık sağlaması durumu trafikte hangi değer ile ifade edilir?`,
    options:[`Bencillik`,`Feragat`,`Diğerkâmlık`,`Sorumsuzluk`], correct:2 },

  { n:48, section:"Trafik Adabı",
    stem:`Sürücüler, trafik adabı açısından başarılı iletişim kurma becerilerini geliştirmek için hangisini yapmalıdır?`,
    options:[`İnsanların değişebileceğine inanmalıdır.`,`Dinlerken aynı zamanda değerlendirme eğiliminde olmalıdır.`,`Karşısındakinin kişiliğini sevmediğinde kendini iletişime kapatmalıdır.`,`Birini anlamak için tek bir olayın yeterli olduğunu düşünmelidir.`], correct:0 },

  { n:49, section:"Araç Tekniği",
    media:{type:"video", file:"images/soru49.mp4"},
    caption:`[Video] Sarı minibüsün seyri.`,
    stem:`Videodaki sarı minibüsle ilgili hangisi kesinlikle söylenir?`,
    options:[`Egzozunun arızalı olduğu`,`Motorunun düzensiz çalıştığı`,`Yüksek devirde kullanıldığı`,`Kapasitesinin üzerinde yük taşıdığı`], correct:1 },

  { n:50, section:"Trafik ve Çevre",
    stem:`I. Orta refüjlere ve yol kenarlarına dikilen ağaçların zarar görmesi
II. Köprü ve tünel gibi noktalarda yaşanan kazalarda ulaşımın aksaması
III. Trafo ve elektrik direğine çarpma gibi durumlarda kesintilerin yaşanması
IV. Yakıt, kimyasal madde, tıbbi atık vs. yüklü araçların yaptığı kazalar neticesinde büyük ekolojik zararların görülmesi

Numaralanmış ifadelerden hangileri kara yolunda meydana gelen trafik kazalarının topluma, kamuya ve çevreye verdiği zararlardandır?`,
    options:[`I ve II`,`I, II ve IV`,`II, III ve IV`,`I, II, III ve IV`], correct:3 }
];
