/* Mobil hamburger menü — 640px altında nav linklerini gizler, toggle ile açar */
(function(){
  var CSS = ''
    + '.menu-toggle{display:none;align-items:center;justify-content:center;width:36px;height:36px;border:none;background:none;cursor:pointer;color:#08090a;padding:0}'
    + '@media(max-width:640px){'
    +   '.nav{display:none!important;position:absolute;top:100%;left:0;right:0;background:#fff;border-bottom:1px solid #ececec;padding:12px 20px;flex-direction:column;gap:0;box-shadow:0 8px 24px rgba(0,0,0,.08);z-index:50}'
    +   '.nav.open{display:flex!important}'
    +   '.nav a{padding:12px 0;border-bottom:1px solid #f5f5f5;font-size:14px!important;white-space:normal}'
    +   '.nav a:last-child{border-bottom:none}'
    +   '.menu-toggle{display:flex}'
    +   'header{position:relative;gap:8px!important;padding-left:12px!important}'
    + '}';

  var style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  var header = document.querySelector('header');
  var nav = header && header.querySelector('.nav');
  if(!header || !nav) return;

  var btn = document.createElement('button');
  btn.className = 'menu-toggle';
  btn.setAttribute('aria-label', 'Menü');
  btn.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';

  // Insert before logo (first child of header)
  header.insertBefore(btn, header.firstElementChild);

  var hamburgerSvg = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
  var closeSvg = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>';

  btn.addEventListener('click', function(e){
    e.stopPropagation();
    var isOpen = nav.classList.toggle('open');
    btn.innerHTML = isOpen ? closeSvg : hamburgerSvg;
  });

  // Close on link click
  nav.addEventListener('click', function(e){
    if(e.target.tagName === 'A'){
      nav.classList.remove('open');
      btn.innerHTML = hamburgerSvg;
    }
  });

  // Close on outside click
  document.addEventListener('click', function(e){
    if(nav.classList.contains('open') && !header.contains(e.target)){
      nav.classList.remove('open');
      btn.innerHTML = hamburgerSvg;
    }
  });
})();
