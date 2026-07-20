/* Ders notu sayfaları için soldan içindekiler (TOC) navigatörü */
(function(){
  var COURSES = [{"course": "Araç Tekniği (Motor)", "lessons": [{"n": 1, "title": "Motor Nedir?", "url": "/dersler/arac-teknigi/motor-nedir/"}, {"n": 2, "title": "Otomatik Vites", "url": "/dersler/arac-teknigi/otomatik-vites/"}, {"n": 3, "title": "Araç Kullanmaya Hazırlık", "url": "/dersler/arac-teknigi/arac-kullanmaya-hazirlik/"}, {"n": 4, "title": "Aydınlatma ve İkaz Sistemi", "url": "/dersler/arac-teknigi/aydinlatma-ve-ikaz-sistemi/"}, {"n": 5, "title": "Fren Sistemi", "url": "/dersler/arac-teknigi/fren-sistemi/"}, {"n": 6, "title": "Lastikler", "url": "/dersler/arac-teknigi/lastikler/"}, {"n": 7, "title": "Ön Düzen ve Direksiyon Sistemi", "url": "/dersler/arac-teknigi/on-duzen-direksiyon/"}, {"n": 8, "title": "Aktif ve Pasif Güvenlik Sistemleri", "url": "/dersler/arac-teknigi/aktif-pasif-guvenlik/"}, {"n": 9, "title": "Derhal Durulması Gereken Haller", "url": "/dersler/arac-teknigi/derhal-durulmasi-gereken-haller/"}, {"n": 10, "title": "Soğutma Sistemleri", "url": "/dersler/arac-teknigi/sogutma-sistemi/"}, {"n": 11, "title": "Ateşleme Sistemi", "url": "/dersler/arac-teknigi/atesleme-sistemi/"}, {"n": 12, "title": "Yağlama Sistemi", "url": "/dersler/arac-teknigi/yaglama-sistemi/"}, {"n": 13, "title": "Şarj Sistemi", "url": "/dersler/arac-teknigi/sarj-sistemi/"}, {"n": 14, "title": "Güç Aktarma Organları", "url": "/dersler/arac-teknigi/guc-aktarma-organlari/"}, {"n": 15, "title": "Süspansiyon Sistemi", "url": "/dersler/arac-teknigi/suspansiyon-sistemi/"}]}, {"course": "Trafik ve Çevre", "lessons": [{"n": 1, "title": "Temel Kavramlar", "url": "/dersler/trafik-ve-cevre/temel-tanimlar/"}, {"n": 2, "title": "Kurum ve Kuruluşlar", "url": "/dersler/trafik-ve-cevre/kurum-ve-kuruluslar/"}, {"n": 3, "title": "Genel Tanımlar", "url": "/dersler/trafik-ve-cevre/genel-tanimlar/"}, {"n": 4, "title": "Araçlarla İlgili Tanımlar", "url": "/dersler/trafik-ve-cevre/araclarla-ilgili-tanimlar/"}, {"n": 5, "title": "Trafik İşaretlerine Uymada Öncelik Sırası", "url": "/dersler/trafik-ve-cevre/oncelik-sirasi/"}, {"n": 6, "title": "Trafik Işıkları", "url": "/dersler/trafik-ve-cevre/trafik-isiklari/"}, {"n": 7, "title": "Araç Kullanma Süreleri ve Yasakları", "url": "/dersler/trafik-ve-cevre/arac-kullanma-sureleri/"}, {"n": 8, "title": "Hız Sınırları", "url": "/dersler/trafik-ve-cevre/hiz-sinirlari/"}, {"n": 9, "title": "Karayolunun Kullanılması", "url": "/dersler/trafik-ve-cevre/karayolunun-kullanilmasi/"}, {"n": 10, "title": "Kavşaklarda İlk Geçiş Hakkı", "url": "/dersler/trafik-ve-cevre/kavsaklarda-gecis-hakki/"}, {"n": 11, "title": "Kontrollü Kavşaklar", "url": "/dersler/trafik-ve-cevre/kontrollu-kavsaklar/"}]}, {"course": "İlk Yardım", "lessons": [{"n": 1, "title": "İlk Yardım ve Acil Tedavi", "url": "/dersler/ilk-yardim/ilk-yardim-ve-acil-tedavi/"}, {"n": 2, "title": "İlk Yardımın ABC'si", "url": "/dersler/ilk-yardim/ilk-yardimin-abcsi/"}, {"n": 3, "title": "Vücudu Oluşturan Sistemler", "url": "/dersler/ilk-yardim/vucudu-olusturan-sistemler/"}, {"n": 4, "title": "Kanamalar", "url": "/dersler/ilk-yardim/kanamalar/"}, {"n": 5, "title": "Turnike Yöntemi", "url": "/dersler/ilk-yardim/turnike/"}, {"n": 6, "title": "Şok, Koma ve Bayılma", "url": "/dersler/ilk-yardim/sok-koma-bayilma/"}, {"n": 7, "title": "Yaralanmalar", "url": "/dersler/ilk-yardim/yaralanmalar/"}, {"n": 8, "title": "Yanıklar", "url": "/dersler/ilk-yardim/yaniklar/"}, {"n": 9, "title": "Kırık, Çıkık, Burkulma", "url": "/dersler/ilk-yardim/kirik-cikik-burkulma/"}, {"n": 10, "title": "Taşıma Teknikleri", "url": "/dersler/ilk-yardim/tasima-teknikleri/"}, {"n": 11, "title": "Yaşam Bulguları", "url": "/dersler/ilk-yardim/yasam-bulgulari/"}, {"n": 12, "title": "Solunum Yolu Tıkanıkları (Heimlich Manevrası)", "url": "/dersler/ilk-yardim/solunum-yolu-tikanikligi/"}]}, {"course": "Trafik Adabı", "lessons": [{"n": 1, "title": "Trafik Adabı ve Temel Kavramlar", "url": "/dersler/trafik-adabi/temel-kavramlar/"}, {"n": 2, "title": "Trafikte İletişim", "url": "/dersler/trafik-adabi/trafikte-iletisim/"}, {"n": 3, "title": "Trafikte Temel Değerler", "url": "/dersler/trafik-adabi/temel-degerler/"}, {"n": 4, "title": "Öfke, Stres ve Dikkat Yönetimi", "url": "/dersler/trafik-adabi/ofke-stres-dikkat/"}, {"n": 5, "title": "Bireysel ve Toplumsal Sorumluluk", "url": "/dersler/trafik-adabi/sorumluluk/"}]}];

  function norm(p){ try{p=decodeURIComponent(p);}catch(e){} return p.replace(/\/+$/,'')+'/'; }
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  var CSS = ''
   + '.toc-bar{display:none;position:sticky;top:64px;z-index:9;background:#fff;border-bottom:1px solid var(--line,#ececec);padding:10px 16px;box-shadow:0 2px 8px rgba(0,0,0,.06)}'
   + '.toc-toggle{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line,#ececec);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:14px;font-weight:500;color:#08090a;cursor:pointer}'
   + '.lesson-layout{display:flex;align-items:stretch;gap:0;max-width:1300px;margin:0 auto;flex:1 0 0}'
   + '.toc{position:sticky;top:64px;align-self:flex-start;width:288px;flex-shrink:0;max-height:calc(100vh - 64px);overflow-y:auto;padding:30px 14px 48px 24px}'
   + '.toc-h{font-family:\'Geist Mono\',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6a6f76;padding:0 10px;margin:0 0 12px}'
   + '.toc-group{margin-bottom:2px}'
   + '.toc-course{width:100%;display:flex;justify-content:space-between;align-items:center;gap:8px;background:none;border:none;cursor:pointer;font:inherit;font-size:13.5px;font-weight:600;color:#08090a;padding:9px 10px;border-radius:8px;text-align:left;letter-spacing:-.01em}'
   + '.toc-course:hover{background:#f5f5f5}'
   + '.toc-caret{transition:transform .2s;color:#9aa0a6;flex-shrink:0}'
   + '.toc-group.open>.toc-course .toc-caret{transform:rotate(90deg)}'
   + '.toc-list{display:none;flex-direction:column;padding:2px 0 10px}'
   + '.toc-group.open>.toc-list{display:flex}'
   + '.toc-link{display:flex;gap:9px;align-items:baseline;padding:6px 10px 6px 14px;font-size:13px;line-height:1.4;color:#5b6169;text-decoration:none;border-radius:7px;border-left:2px solid transparent;margin-left:4px}'
   + '.toc-link:hover{background:#f5f5f5;color:#08090a}'
   + '.toc-link.active{color:#08090a;font-weight:600;border-left-color:#08090a;background:#f5f5f5}'
   + '.toc-n{font-family:\'Geist Mono\',monospace;font-size:11px;color:#9aa0a6;min-width:18px;flex-shrink:0}'
   + '.lesson-layout>main{margin:0;max-width:840px;flex:1;min-width:0;border-left:1px solid var(--line,#ececec)}'
   + '.pn-nav{display:flex;gap:14px;margin-top:22px}'
   + '.pn{flex:1;min-width:0;display:flex;flex-direction:column;gap:5px;border:1px solid var(--line,#ececec);border-radius:14px;padding:15px 18px;text-decoration:none;color:inherit;transition:.15s}'
   + 'a.pn:hover{border-color:#d4d4d4;box-shadow:0 8px 22px rgba(0,0,0,.05)}'
   + '.pn-k{font-family:\'Geist Mono\',monospace;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:#6a6f76}'
   + '.pn-t{font-weight:600;font-size:14px;letter-spacing:-.015em;color:#08090a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}'
   + '.pn.next{text-align:right;align-items:flex-end}'
   + '.pn-empty{border:none;box-shadow:none;pointer-events:none}'
   + '@media(max-width:980px){'
   +   '.toc-bar{display:block;position:static;box-shadow:none}'
   +   '.lesson-layout{flex-direction:column}'
   +   '.toc{position:static;width:100%;max-height:none;border-bottom:1px solid var(--line,#ececec);display:none;padding:16px 18px 22px}'
   +   '.lesson-layout>main{border-left:none}'
   +   '.toc.open{display:block}'
   +   '.lesson-layout>main{max-width:100%;padding-top:12px}'
   + '}'
   + '@media(max-width:640px){.pn-nav{flex-direction:column}.pn-empty{display:none}}';

  function build(){
    var main = document.querySelector('main');
    if(!main) return;
    var here = norm(location.pathname);

    var style=document.createElement('style'); style.textContent=CSS; document.head.appendChild(style);

    // mobil aç/kapa çubuğu
    var bar=document.createElement('div'); bar.className='toc-bar';
    bar.innerHTML='<button class="toc-toggle" id="tocToggle"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg> Konular</button>';

    // layout sarmalayıcı
    var layout=document.createElement('div'); layout.className='lesson-layout';
    var aside=document.createElement('aside'); aside.className='toc';

    var htmlParts=['<p class="toc-h">Ders Notları</p>'];
    COURSES.forEach(function(c){
      var isCur = c.lessons.some(function(l){ return norm(l.url)===here; });
      htmlParts.push('<div class="toc-group'+(isCur?' open':'')+'">');
      htmlParts.push('<button class="toc-course" type="button"><span>'+esc(c.course)+'</span>'
        +'<svg class="toc-caret" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></button>');
      htmlParts.push('<div class="toc-list">');
      c.lessons.forEach(function(l){
        var act = norm(l.url)===here;
        htmlParts.push('<a class="toc-link'+(act?' active':'')+'" href="'+l.url+'"'+(act?' aria-current="page"':'')+'>'
          +'<span class="toc-n">'+String(l.n).padStart(2,'0')+'</span><span>'+esc(l.title)+'</span></a>');
      });
      htmlParts.push('</div></div>');
    });
    aside.innerHTML=htmlParts.join('');

    main.parentNode.insertBefore(bar, main);
    main.parentNode.insertBefore(layout, main);
    layout.appendChild(aside);
    layout.appendChild(main);

    // kurs grubu aç/kapa
    aside.addEventListener('click', function(e){
      var btn=e.target.closest('.toc-course'); if(!btn) return;
      btn.parentNode.classList.toggle('open');
    });
    // mobil aç/kapa
    document.getElementById('tocToggle').addEventListener('click', function(){ aside.classList.toggle('open'); });

    // aktif linki görünür kıl
    var act=aside.querySelector('.toc-link.active');
    if(act) act.scrollIntoView({block:'center'});

    // önceki / sonraki konu yönlendirmesi (kısa testin hemen altında)
    var arr=null, ci=-1;
    for(var gi=0; gi<COURSES.length && !arr; gi++){
      var ls=COURSES[gi].lessons;
      for(var li=0; li<ls.length; li++){ if(norm(ls[li].url)===here){ arr=ls; ci=li; break; } }
    }
    if(arr && (ci>0 || ci<arr.length-1)){
      var prev = ci>0 ? arr[ci-1] : null;
      var next = ci<arr.length-1 ? arr[ci+1] : null;
      var pn=document.createElement('nav'); pn.className='pn-nav';
      var parts=[];
      parts.push(prev
        ? '<a class="pn prev" href="'+prev.url+'"><span class="pn-k">← Önceki Konu</span><span class="pn-t">'+esc(prev.title)+'</span></a>'
        : '<span class="pn pn-empty"></span>');
      parts.push(next
        ? '<a class="pn next" href="'+next.url+'"><span class="pn-k">Sonraki Konu →</span><span class="pn-t">'+esc(next.title)+'</span></a>'
        : '<span class="pn pn-empty"></span>');
      pn.innerHTML=parts.join('');
      var cta=main.querySelector('.quiz-cta');
      if(cta) cta.parentNode.insertBefore(pn, cta.nextSibling);
      else main.appendChild(pn);
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
