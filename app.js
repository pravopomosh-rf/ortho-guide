function setL(l){document.body.className=l;var d=l=='ru'?'ltr':'rtl';document.documentElement.dir=d;document.documentElement.lang=l;
document.querySelectorAll('.lang button').forEach(function(b){b.classList.toggle('on',b.dataset.k==l)});try{localStorage.lang=l}catch(e){}
document.querySelectorAll('video').forEach(function(v){if(!v.closest('[data-l='+l+']'))v.pause()})}
function seek(l,t){var v=document.getElementById('v_'+l);v.currentTime=t;v.play();return false}
var q=(location.hash.match(/lang=(ru|he|ar)/)||[])[1];setL(q||(function(){try{return localStorage.lang}catch(e){}})()||'he');
(function(){if(!/[?&#]v=1/.test(location.search+location.hash))return;function go(){var l=document.body.className||'he',e=document.getElementById('video_'+l);if(e)e.scrollIntoView({behavior:'smooth',block:'start'})}if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',go);else go();setTimeout(go,400)})();

/* ---- Visual enhancement only: icons beside headings, warning tones, gentle reveal.
   Does not change any text. Section type is chosen from the Russian heading and applied
   to the same section id in he/ar, so all three languages look identical. ---- */
(function(){
var P='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">',E='</svg>';
var I={
 joint:'<circle cx="12" cy="8" r="3.2"/><path d="M12 11.2V21M8.5 4.5a5 5 0 0 1 7 0M7 21h10"/>',
 prep:'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M8.5 11l2 2 4-4M8.5 17h7"/>',
 pill:'<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="M9.3 8.1l5.4 7.8"/>',
 drop:'<path d="M12 3s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11z"/><path d="M9.5 15a2.6 2.6 0 0 0 2.5 2.5"/>',
 play:'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9.2v5.6l4.6-2.8z"/>',
 book:'<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 alert:'<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.4v.1"/>',
 phone:'<path d="M6.5 3.5h3l1.5 4.5-2 1.5a11 11 0 0 0 5.5 5.5l1.5-2 4.5 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5.5a2 2 0 0 1 2-2z"/>',
 hosp:'<path d="M4 21V7l8-4 8 4v14M2.5 21h19M12 9v6M9 12h6"/>',
 clock:'<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 leaf:'<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19c3-4 6-6.5 9-8"/>',
 band:'<rect x="2.5" y="8" width="19" height="8" rx="4" transform="rotate(-30 12 12)"/><path d="M10.5 10.8v.1M13.5 13.2v.1M10.5 13.2v.1M13.5 10.8v.1"/>',
 info:'<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8v.1"/>',
 bag:'<rect x="4" y="7.5" width="16" height="13" rx="2.5"/><path d="M9 7.5V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5v2M4 13h16"/>',
 id:'<path d="M3 12a9 4 0 0 0 18 0"/><path d="M3 12a9 4 0 0 1 18 0"/><rect x="9" y="10" width="6" height="4" rx="1"/>',
 smoke:'<path d="M3 15h13v3H3zM19 15v3M3.5 3.5l17 17"/><path d="M18 11c0-2-2-2-2-4"/>',
 xray:'<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/><path d="M9 7v4l-2 6M15 7v4l2 6M9 11h6"/>',
 food:'<path d="M7 3v7a2 2 0 0 0 4 0V3M9 10v11M16 3c-2 1.5-2 6 0 8v10"/>',
 mind:'<path d="M9 21v-3.5A7 7 0 1 1 18 14l1.5 3h-3.5v4z"/><path d="M10 9.5a2 2 0 1 1 2 2v1.5"/>',
 syr:'<path d="M17 3l4 4M19 5l-9.5 9.5M14 4l6 6M6.5 13.5l4 4M8 15.5l-4.5 4.5M11.5 8.5l1.5 1.5M9.5 10.5l1.5 1.5"/>',
 people:'<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0M16 5.2a3 3 0 0 1 0 5.6M21 20a6 6 0 0 0-3.5-5.4"/>',
 move:'<circle cx="13" cy="4.5" r="1.8"/><path d="M8 21l3-6 3 2v4M11 15l1-6 4 3h3M12 9l-4 1-2 3"/>',
 scale:'<path d="M12 4v16M6 20h12M4.5 8h15M7 8l-3 6a3 3 0 0 0 6 0zM17 8l-3 6a3 3 0 0 0 6 0z"/>',
 spine:'<path d="M12 2.5v19"/><rect x="8.5" y="4" width="7" height="3.4" rx="1.5"/><rect x="8" y="10.3" width="8" height="3.4" rx="1.5"/><rect x="8.5" y="16.6" width="7" height="3.4" rx="1.5"/>',
 wound:'<rect x="3" y="8" width="18" height="8" rx="4"/><path d="M10 8v8M14 8v8"/>'
};
function ico(k){return P+(I[k]||I.info)+E}
/* [regex on Russian heading, icon, tone] — first match wins */
var R=[
 [/101/,'phone','warn'],
 [/приёмный покой|приемный покой/i,'hosp','warn'],
 [/срочно/i,'alert','warn'],
 [/в тот же день|когда сообщить/i,'clock','caution'],
 [/нормально/i,'leaf','calm'],
 [/рана|тромб/i,'wound'],
 [/источник/i,'book'],
 [/видео/i,'play'],
 [/лекарств|обезбол/i,'pill'],
 [/клексан/i,'syr'],
 [/дренаж/i,'drop'],
 [/еда|питьё/i,'food'],
 [/кур/i,'smoke'],
 [/браслет/i,'id'],
 [/взять/i,'bag'],
 [/кож|душ|подготов/i,'prep'],
 [/делирий|спутанн/i,'mind'],
 [/рентген|выглядит/i,'xray'],
 [/для кого/i,'people'],
 [/восстан|движени|выписк|после операции/i,'move'],
 [/ожидани|обсуждают/i,'scale'],
 [/осложнени/i,'info'],
 [/сустав|операци|перелом|доступ|эндопротез|изношенн/i,'joint']
];
var tones={},icons={};
document.querySelectorAll('[data-l=ru] section').forEach(function(s,n){
 var h=s.querySelector('h2');if(!h)return;var t=h.textContent,key=s.id?s.id.replace(/_ru$/,''):'#'+n;
 for(var i=0;i<R.length;i++)if(R[i][0].test(t)){icons[key]=R[i][1];tones[key]=R[i][2];break}
});
['ru','he','ar'].forEach(function(l){
 var wrap=document.querySelector('main>[data-l='+l+']');if(!wrap)return;
 wrap.querySelectorAll(':scope>section').forEach(function(s,n){
  var key=s.id?s.id.replace(/_(ru|he|ar)$/,''):'#'+n,h=s.querySelector('h2');
  if(!h||!icons[key])return;
  h.classList.add('ic');h.insertAdjacentHTML('afterbegin',ico(icons[key]));
  if(tones[key])s.classList.add(tones[key]);
 });
 /* home topic headings: same order in every language */
 var th=['joint','xray','spine','prep','move','alert','people'];
 wrap.querySelectorAll('h2.topich').forEach(function(h,i){h.insertAdjacentHTML('afterbegin',ico(th[i]||'info'))});
});

/* gentle reveal on scroll; skipped entirely when the user prefers reduced motion */
var mq=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)');
if(!('IntersectionObserver' in window)||(mq&&mq.matches))return;
document.documentElement.classList.add('js');
var els=document.querySelectorAll('main section,main a.op,main figure,main .topich,main .disc,main .soon');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight){e.classList.add('rv','in')}else{e.classList.add('rv');io.observe(e)}});
})();
