/* Ders notu sayfaları için soldan içindekiler (TOC) navigatörü */
(function(){
  var COURSES = [{"course": "Araç Tekniği (Motor)", "lessons": [{"n": 1, "title": "Motor Nedir?", "url": "/arac_teknigi/ders_1/motor_nedir/"}, {"n": 2, "title": "Otomatik Vites", "url": "/arac_teknigi/ders_2/otomatik_vites/"}, {"n": 3, "title": "Araç Kullanmaya Hazırlık", "url": "/arac_teknigi/ders_3/arac_kullanmaya_hazirlik/"}, {"n": 4, "title": "Aydınlatma ve İkaz Sistemi", "url": "/arac_teknigi/ders_4/aydinlatma_ve_ikaz_sistemi/"}, {"n": 5, "title": "Fren Sistemi", "url": "/arac_teknigi/ders_5/fren_sistemi/"}, {"n": 6, "title": "Lastikler", "url": "/arac_teknigi/ders_6/lastikler/"}, {"n": 7, "title": "Ön Düzen ve Direksiyon Sistemi", "url": "/arac_teknigi/ders_7/on_duzen_direksiyon/"}, {"n": 8, "title": "Aktif ve Pasif Güvenlik Sistemleri", "url": "/arac_teknigi/ders_8/aktif_pasif_guvenlik/"}, {"n": 9, "title": "Derhal Durulması Gereken Haller", "url": "/arac_teknigi/ders_9/derhal_durulmasi_gereken_haller/"}, {"n": 10, "title": "Soğutma Sistemleri", "url": "/arac_teknigi/ders_10/sogutma_sistemi/"}, {"n": 11, "title": "Ateşleme Sistemi", "url": "/arac_teknigi/ders_11/atesleme_sistemi/"}, {"n": 12, "title": "Yağlama Sistemi", "url": "/arac_teknigi/ders_12/yaglama_sistemi/"}, {"n": 13, "title": "Şarj Sistemi", "url": "/arac_teknigi/ders_13/sarj_sistemi/"}, {"n": 14, "title": "Güç Aktarma Organları", "url": "/arac_teknigi/ders_14/guc_aktarma_organlari/"}, {"n": 15, "title": "Süspansiyon Sistemi", "url": "/arac_teknigi/ders_15/suspansiyon_sistemi/"}]}, {"course": "Trafik ve Çevre", "lessons": [{"n": 1, "title": "Temel Kavramlar", "url": "/trafik_ve_cevre/ders_1/temel_tanımlar/"}, {"n": 2, "title": "Kurum ve Kuruluşlar", "url": "/trafik_ve_cevre/ders_2/kurum_ve_kuruluslar/"}, {"n": 3, "title": "Genel Tanımlar", "url": "/trafik_ve_cevre/ders_3/genel_tanimlar/"}, {"n": 4, "title": "Araçlarla İlgili Tanımlar", "url": "/trafik_ve_cevre/ders_4/araclarla_ilgili_tanimlar/"}, {"n": 5, "title": "Trafik İşaretlerine Uymada Öncelik Sırası", "url": "/trafik_ve_cevre/ders_5/oncelik_sirasi/"}, {"n": 6, "title": "Trafik Işıkları", "url": "/trafik_ve_cevre/ders_6/trafik_isiklari/"}, {"n": 7, "title": "Araç Kullanma Süreleri ve Yasakları", "url": "/trafik_ve_cevre/ders_7/arac_kullanma_sureleri/"}, {"n": 8, "title": "Hız Sınırları", "url": "/trafik_ve_cevre/ders_8/hiz_sinirlari/"}, {"n": 9, "title": "Karayolunun Kullanılması", "url": "/trafik_ve_cevre/ders_9/karayolunun_kullanilmasi/"}, {"n": 10, "title": "Kavşaklarda İlk Geçiş Hakkı", "url": "/trafik_ve_cevre/ders_10/kavsaklarda_gecis_hakki/"}, {"n": 11, "title": "Kontrollü Kavşaklar", "url": "/trafik_ve_cevre/ders_11/kontrollu_kavsaklar/"}]}, {"course": "İlk Yardım", "lessons": [{"n": 1, "title": "İlk Yardım ve Acil Tedavi", "url": "/ilk_yardim/ders_1/ilk_yardim_ve_acil_tedavi/"}, {"n": 2, "title": "İlk Yardımın ABC'si", "url": "/ilk_yardim/ders_2/ilk_yardimin_abcsi/"}, {"n": 3, "title": "Vücudu Oluşturan Sistemler", "url": "/ilk_yardim/ders_3/vucudu_olusturan_sistemler/"}, {"n": 4, "title": "Kanamalar", "url": "/ilk_yardim/ders_4/kanamalar/"}, {"n": 5, "title": "Turnike Yöntemi", "url": "/ilk_yardim/ders_5/turnike/"}, {"n": 6, "title": "Şok, Koma ve Bayılma", "url": "/ilk_yardim/ders_6/sok_koma_bayilma/"}, {"n": 7, "title": "Yaralanmalar", "url": "/ilk_yardim/ders_7/yaralanmalar/"}, {"n": 8, "title": "Yanıklar", "url": "/ilk_yardim/ders_8/yaniklar/"}, {"n": 9, "title": "Kırık, Çıkık, Burkulma", "url": "/ilk_yardim/ders_9/kirik_cikik_burkulma/"}, {"n": 10, "title": "Taşıma Teknikleri", "url": "/ilk_yardim/ders_10/tasima_teknikleri/"}, {"n": 11, "title": "Yaşam Bulguları", "url": "/ilk_yardim/ders_11/yasam_bulgulari/"}, {"n": 12, "title": "Solunum Yolu Tıkanıkları (Heimlich Manevrası)", "url": "/ilk_yardim/ders_12/solunum_yolu_tikanikligi/"}]}, {"course": "Trafik Adabı", "lessons": [{"n": 1, "title": "Trafik Adabı ve Temel Kavramlar", "url": "/trafik_adabi/ders_1/temel_kavramlar/"}, {"n": 2, "title": "Trafikte İletişim", "url": "/trafik_adabi/ders_2/trafikte_iletisim/"}, {"n": 3, "title": "Trafikte Temel Değerler", "url": "/trafik_adabi/ders_3/temel_degerler/"}, {"n": 4, "title": "Öfke, Stres ve Dikkat Yönetimi", "url": "/trafik_adabi/ders_4/ofke_stres_dikkat/"}, {"n": 5, "title": "Bireysel ve Toplumsal Sorumluluk", "url": "/trafik_adabi/ders_5/sorumluluk/"}]}];

  function norm(p){ try{p=decodeURIComponent(p);}catch(e){} return p.replace(/\/+$/,'')+'/'; }
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  var CSS = ''
   + '.toc-bar{display:none;position:sticky;top:64px;z-index:9;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line,#ececec);padding:10px 16px}'
   + '.toc-toggle{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line,#ececec);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:14px;font-weight:500;color:#08090a;cursor:pointer}'
   + '.lesson-layout{display:flex;align-items:flex-start;gap:0;max-width:1300px;margin:0 auto}'
   + '.toc{position:sticky;top:64px;align-self:flex-start;width:288px;flex-shrink:0;max-height:calc(100vh - 64px);overflow-y:auto;padding:30px 14px 48px 24px;border-right:1px solid var(--line,#ececec)}'
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
   + '.lesson-layout>main{margin:0;max-width:840px;flex:1;min-width:0}'
   + '.pn-nav{display:flex;gap:14px;margin-top:22px}'
   + '.pn{flex:1;min-width:0;display:flex;flex-direction:column;gap:5px;border:1px solid var(--line,#ececec);border-radius:14px;padding:15px 18px;text-decoration:none;color:inherit;transition:.15s}'
   + 'a.pn:hover{border-color:#d4d4d4;box-shadow:0 8px 22px rgba(0,0,0,.05)}'
   + '.pn-k{font-family:\'Geist Mono\',monospace;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:#6a6f76}'
   + '.pn-t{font-weight:600;font-size:14px;letter-spacing:-.015em;color:#08090a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}'
   + '.pn.next{text-align:right;align-items:flex-end}'
   + '.pn-empty{border:none;box-shadow:none;pointer-events:none}'
   + '@media(max-width:980px){'
   +   '.toc-bar{display:block}'
   +   '.lesson-layout{flex-direction:column}'
   +   '.toc{position:static;width:auto;max-height:none;border-right:none;border-bottom:1px solid var(--line,#ececec);display:none;padding:16px 18px 22px}'
   +   '.toc.open{display:block}'
   +   '.lesson-layout>main{max-width:100%}'
   + '}'
   + '@media(max-width:640px){.pn-nav{flex-direction:column}.pn-empty{display:none}.toc-bar{top:58px}}';

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
