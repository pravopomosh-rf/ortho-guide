document.documentElement.classList.add('js');
function setL(l){document.body.className=l;var d=(l=='ru'||l=='en')?'ltr':'rtl';document.documentElement.dir=d;document.documentElement.lang=l;
document.querySelectorAll('.lang button').forEach(function(b){b.classList.toggle('on',b.dataset.k==l);b.setAttribute('aria-pressed',b.dataset.k==l?'true':'false')});var h1=document.querySelector('header [data-l='+l+'] h1');if(h1)document.title=h1.textContent.trim();try{localStorage.lang=l}catch(e){}
var fv=0;document.querySelectorAll('video:not(.hero)').forEach(function(v){if(v.closest('[data-l='+l+']')){if(!fv&&v.preload=='none')v.preload='metadata';fv=1}else{v.pause();if(v.networkState!=1)v.preload='none'}});
if(window.__rv)window.__rv()}
function seek(l,t){var v=document.getElementById('v_'+l);v.currentTime=t;v.play();return false}

/* ===== Оформление: иконки, цвет тревоги, рассвет, появление блоков (тексты страниц не меняются) ===== */
(function(){
var P={
info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5v.5"/>',
check:'<rect x="5" y="4" width="14" height="17" rx="2.5"/><path d="M9 4.5V3h6v1.5M8.5 11.5l2 2 4-4M8.5 17h7"/>',
pill:'<rect x="3.5" y="8.5" width="17" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="M9.6 8.6l4.8 6.8"/>',
drop:'<path d="M12 3.5c3.2 4 5.5 7 5.5 10a5.5 5.5 0 0 1-11 0c0-3 2.3-6 5.5-10z"/>',
shower:'<path d="M4 20V8a4 4 0 0 1 8 0"/><path d="M9 8h6"/><path d="M11 12v1M14 12v1M17 12v1M12 16v1M15 16v1M18 16v1"/>',
cup:'<path d="M5 8h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z"/><path d="M16 9.5h1.5a2.5 2.5 0 0 1 0 5H16M8 3.5v2M11 3.5v2"/>',
bag:'<rect x="4" y="7.5" width="16" height="12.5" rx="2.5"/><path d="M9 7.5V5.5a3 3 0 0 1 6 0v2"/>',
tag:'<rect x="3" y="8" width="18" height="8" rx="4"/><path d="M8 12h5"/>',
nosmoke:'<rect x="3" y="12" width="14" height="4" rx="1"/><path d="M19 12v4M17 6c0 2 2 2 2 4M3 3l18 18"/>',
bandage:'<rect x="2.5" y="8" width="19" height="8" rx="4" transform="rotate(-45 12 12)"/><path d="M10.5 10.5h.01M13.5 13.5h.01M13.5 10.5h.01M10.5 13.5h.01"/>',
heart:'<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.6 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/>',
people:'<circle cx="9" cy="8" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9" r="2.3"/><path d="M15.5 14.2a4.5 4.5 0 0 1 5 4.8"/>',
image:'<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="M20 16l-4.5-4.5L7 19.5"/>',
joint:'<circle cx="12" cy="8" r="3.5"/><path d="M12 11.5V21M7.5 5.5c-2 1-3 3-2.5 5M16.5 5.5c2 1 3 3 2.5 5"/>',
bone:'<path d="M8.5 15.5l7-7M6.2 13.2a2.2 2.2 0 1 0 2.6 3.6 2.2 2.2 0 1 0 2.6 2.6M17.8 10.8a2.2 2.2 0 1 0-2.6-3.6 2.2 2.2 0 1 0-2.6-2.6"/><path d="M14.5 8.5l-2-2M9.5 15.5l2 2"/>',
spine:'<rect x="9" y="2.5" width="6" height="3.6" rx="1.3"/><rect x="8.5" y="7.6" width="7" height="3.6" rx="1.3"/><rect x="8.5" y="12.8" width="7" height="3.6" rx="1.3"/><rect x="9" y="18" width="6" height="3.6" rx="1.3"/>',
sun:'<path d="M3 18h18M7 18a5 5 0 0 1 10 0M12 6v3M5.6 10.6l1.8 1.8M18.4 10.6l-1.8 1.8"/>',
shield:'<path d="M12 3l7.5 3v5.5c0 4.5-3.2 7.9-7.5 9.5-4.3-1.6-7.5-5-7.5-9.5V6z"/><path d="M12 8.5v4M12 15.5v.5"/>',
walk:'<circle cx="13" cy="4.5" r="2"/><path d="M10 21l2.5-6.5L15 17v4M8 11l3-3.5 3 1.5 2 3M12.5 14.5l-1-6"/>',
cal:'<rect x="4" y="5.5" width="16" height="15" rx="2.5"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>',
play:'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10.5 9.2v5.6l4.6-2.8z"/>',
book:'<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20v3H6.5"/>',
alert:'<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.2v.3"/>',
phone:'<path d="M6.5 3.5h3l1.5 4.5-2 1.3a10.5 10.5 0 0 0 5.7 5.7l1.3-2 4.5 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5.5a2 2 0 0 1 2-2z"/>',
hosp:'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/>',
leaf:'<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19l7-7"/>'};
function ic(n){return '<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'+(P[n]||P.info)+'</svg></span>'}
var R=[
[/^Call 101/,'phone','danger'],[/right away|immediately|urgent/i,'alert','danger'],[/same day|tell the ward/i,'phone','warn'],[/is normal/i,'heart','calm'],[/^Video/,'play'],[/sources/i,'book'],[/[Mm]edicine|Clexane/,'pill'],[/[Dd]rain/,'drop'],[/wash with|[Ww]ipes|[Ss]kin|[Ss]hower/,'shower'],[/^Food/,'cup'],[/bring/,'bag'],[/wristband/,'tag'],[/[Ss]moking/,'nosmoke'],[/wound/i,'bandage'],[/delirium/,'people'],[/X-ray|looks like/,'image'],[/implant|joint|replacement|anterior approach/i,'joint'],[/complications|risk/i,'shield'],[/[Mm]ovements/,'walk'],[/[Pp]repar/,'check'],[/[Aa]fter surgery|recover|discharge/,'sun'],[/fracture/i,'bone'],[/emergency department to/,'hosp'],[/^(What|Who)/,'info'],[/^When/,'cal'],[/waiting|Modern|Types/,'leaf'],
[/101/,'phone','danger'],
[/срочн|немедленно|בדחיפות|דחופה|(^|\s)מיד|فور|عاجل/i,'alert','danger'],
[/в тот же день|באותו יום|اليوم نفسه/,'phone','warn'],
[/Когда сообщить|מתי להודיע|متى تبلغون/,'phone','warn'],
[/нормально|תקין|طبيعي/,'heart','calm'],
[/Видео|סרטון|فيديو/,'play'],[/источник|מקורות|مصادر/,'book'],
[/Лекарств|лекарств|תרופות|أدوية|الأدوية|Клексан|קלקסן|كليكسان/,'pill'],
[/Дренаж|נקז|تصريف/,'drop'],[/Чем мыться|במה להתקלח|بماذا تستحمون|Салфетки|מגבונים|مناديل/,'shower'],[/кож|Душ|העור|מקלחת|الجلد|الاستحمام/,'shower'],
[/Еда|אוכל|الطعام/,'cup'],[/взять|להביא|تحضرون/,'bag'],[/браслет|צמיד|سوار/,'tag'],
[/Курени|עישון|التدخين/,'nosmoke'],[/Рана|הפצע|الجرح/,'bandage'],
[/делирий|דליריום|الهذيان/,'people'],[/рентген|רנטגן|الأشعة|выглядит|נראית|تبدو/,'image'],
[/Эндопротез|תותבת|صناعي/,'joint'],[/осложнен|סיבוכים|المضاعفات/,'shield'],
[/Движени|תנועות|الحركة/,'walk'],[/риск|הסיכון|الخطر/,'shield'],
[/Подготов|подготов|להתכונן|הכנה|التحضير|تستعدون/,'check'],
[/После|после|восстанав|выпис|אחרי|מחלימים|החלמה|השחרור|بعد|تتعاف|التعافي|الخروج/,'sun'],
[/сустав|מפרק|مفصل|доступ|גישה|المدخل/,'joint'],[/перелом|השבר|الكسر/,'bone'],
[/приёмного|מהמיון|الطوارئ إلى/,'hosp'],[/Что это|Что такое|Что происходит|Для кого|^מה |^מהי|למי|^ما |لمن/,'info'],[/Когда|מתי|متى/,'cal'],[/ожидани|ההמתנה|الانتظار|операция$|הניתוח כיום|العملية اليوم/,'leaf']];
function pick(t){for(var i=0;i<R.length;i++)if(R[i][0].test(t))return R[i];return [0,'info']}
document.querySelectorAll('section>h2').forEach(function(h){var r=pick(h.textContent);h.insertAdjacentHTML('afterbegin',ic(r[1]));if(r[2])h.parentNode.classList.add(r[2])});
var T=[[/^Joints/,'joint'],[/^Fractures/,'bone'],[/^Spine/,'spine'],[/^Preparing/,'check'],[/^After/,'sun'],[/101/,'alert'],[/^General/,'leaf'],[/Суставы|מפרקים|المفاصل/,'joint'],[/Перелом|שברים|الكسور/,'bone'],[/Позвоночник|עמוד השדרה|العمود الفقري/,'spine'],[/Подготовка|הכנה|التحضير/,'check'],[/После|אחרי|بعد/,'sun'],[/101/,'alert'],[/Общие|כלליים|عامة/,'leaf']];
document.querySelectorAll('h2.topich').forEach(function(h){for(var i=0;i<T.length;i++)if(T[i][0].test(h.textContent)){h.insertAdjacentHTML('afterbegin',ic(T[i][1]));break}});
var A=[[/postop/,'alert'],[/v=1/,'play'],[/thr|tkr/,'joint'],[/hip-fracture/,'bone'],[/kypho|lamin|fusion|spine/,'spine'],[/preop/,'check'],[/why-wait/,'leaf']];
document.querySelectorAll('a.op').forEach(function(a){var h=a.getAttribute('href'),n='info';for(var i=0;i<A.length;i++)if(A[i][0].test(h)){n=A[i][1];break}
a.innerHTML=ic(n)+'<span class="tx">'+a.innerHTML+'</span>';if(/postop/.test(h))a.classList.add('urgent')});
/* главная: рассвет + подзаголовок */
var hd=document.querySelector('header');
if(hd&&!document.querySelector('header .back')){
var tg={en:'Your surgery explained clearly, step by step',ru:'Понятно о вашей операции — шаг за шагом',he:'הסבר ברור על הניתוח שלכם — צעד אחר צעד',ar:'شرح واضح لعمليتكم — خطوة بخطوة'};
hd.querySelectorAll('[data-l]').forEach(function(d){d.insertAdjacentHTML('beforeend','<p class="tag">'+tg[d.dataset.l]+'</p>')});
hd.querySelector('.lang').insertAdjacentHTML('beforebegin',heroSVG()+'<p class="herocap"><span data-l="en">Everyone recovers differently. Agree with your doctor or physiotherapist on when to change walking aids and when to walk without them.</span><span data-l="ru">Восстановление у каждого проходит по-разному. Переход между средствами опоры и ходьбу без них согласуйте с врачом или физиотерапевтом.</span><span data-l="he">ההחלמה שונה אצל כל אחד. את המעבר בין אמצעי העזר להליכה ואת ההליכה בלעדיהם תאמו עם הרופא או הפיזיותרפיסט.</span><span data-l="ar">يختلف التعافي من شخص لآخر. نسّقوا الانتقال بين وسائل المساعدة على المشي والمشي من دونها مع الطبيب أو أخصائي العلاج الطبيعي.</span></p>');startHero()}
function startHero(){var v=document.querySelector('video.hero');if(!v)return;v.muted=true;v.defaultMuted=true;var p=v.play();if(p&&p.catch)p.catch(function(){})}
function heroSVG(){var B=document.querySelector('header .lang')?'':'';var base=location.pathname.indexOf('/ops/')>-1?'../':'';
var red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
if(red)return '<img class="hero hv" src="'+base+'media/video/hero_end.webp" width="720" height="360" alt="">';
return '<video class="hero hv" autoplay muted playsinline preload="auto" width="720" height="360" poster="'+base+'media/video/hero_start.webp" aria-hidden="true"><source src="'+base+'media/video/hero.webm" type="video/webm"><source src="'+base+'media/video/hero.mp4" type="video/mp4"></video>'}
/* мягкое появление */
var els=[].slice.call(document.querySelectorAll('main section,main a.op,main figure,main .soon,main .disc'));
els.forEach(function(e){e.classList.add('rv')});
var red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
if(red||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -6% 0px'});
window.__rv=function(){els.forEach(function(e){if(!e.classList.contains('in'))io.observe(e)})};window.__rv();
setTimeout(function(){els.forEach(function(e){if(e.getBoundingClientRect().top<innerHeight)e.classList.add('in')})},60)}
})();

var q=(location.hash.match(/lang=(ru|he|ar|en)/)||[])[1];setL(q||(function(){try{return localStorage.lang}catch(e){}})()||'he');
(function(){if(!/[?&#]v=1/.test(location.search+location.hash))return;function go(){var l=document.body.className||'he',e=document.getElementById('video_'+l);if(e)e.scrollIntoView({behavior:'smooth',block:'start'})}if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',go);else go();setTimeout(go,400)})();
/* 04.11: duration on the video label */
document.querySelectorAll('.vtop').forEach(function(s){var v=s.querySelector('video'),d=s.querySelector('.vdur');if(!v||!d)return;function f(){if(!isFinite(v.duration))return;var t=Math.floor(v.duration),m=Math.floor(t/60),x=t%60;d.textContent='· '+m+':'+(x<10?'0':'')+x}v.addEventListener('loadedmetadata',f);f()});

/* 07.11: одновременно играет только одно видео */
document.addEventListener('play',function(e){var t=e.target;if(t.tagName!='VIDEO'||t.classList.contains('hero'))return;document.querySelectorAll('video:not(.hero)').forEach(function(v){if(v!==t&&!v.paused)v.pause()})},true);

/* 08.11: #lang=xx&to=s1 — прокрутка к разделу на нужном языке */
(function(){var m=location.hash.match(/to=([a-z0-9]+)/);if(!m)return;function go(){var l=document.body.className.split(' ')[0]||'he',e=document.getElementById(m[1]+'_'+l);if(e)e.scrollIntoView({block:'start'})}if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',go);else go();setTimeout(go,500)})();

/* 08.11 (аудит): язык меняется при ручной смене #lang= без перезагрузки */
window.addEventListener('hashchange',function(){var q=(location.hash.match(/lang=(ru|he|ar|en)/)||[])[1];if(q&&q!=document.body.className.split(' ')[0])setL(q)});
/* 08.11 (аудит): «101» в тексте — кнопка звонка; в разделах тревоги — крупная красная кнопка */
(function(){
var CALL={ru:'Позвонить 101',he:'להתקשר ל־101',ar:'اتصلوا بـ 101',en:'Call 101'};
function wrap(root){var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),list=[],n;
while(n=w.nextNode()){if(/(^|[^\d])101([^\d]|$)/.test(n.nodeValue)&&!n.parentNode.closest('a,button,header,h1,h2,h3'))list.push(n)}
list.forEach(function(t){var f=document.createDocumentFragment(),parts=t.nodeValue.split(/(101)/);parts.forEach(function(x,i){if(x==='101'&&!/\d$/.test(parts[i-1]||'')&&!/^\d/.test(parts[i+1]||'')){var a=document.createElement('a');a.href='tel:101';a.className='tel';a.textContent='101';f.appendChild(a)}else f.appendChild(document.createTextNode(x))});t.parentNode.replaceChild(f,t)})}
var m=document.querySelector('main');if(!m)return;wrap(m);
document.querySelectorAll('main section.danger').forEach(function(sec){if(!sec.querySelector('a.tel'))return;var d=sec.closest('[data-l]'),l=d?d.getAttribute('data-l'):'he';var b=document.createElement('a');b.href='tel:101';b.className='callbtn';b.innerHTML='<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg><span>'+CALL[l]+'</span>';sec.appendChild(b)});
})();
/* фото страницы: шапка с фото, фото-обложка, прозрачный фон разделов, плавное появление */
(function(){
var pg=(location.pathname.match(/ops\/([a-z0-9-]+)\.html/)||[])[1];if(!pg||pg=='sitemap')return;
var OWN=/*OWN*/[];
var SEC={'thr':'sec_hip','thr-anterior':'sec_hip','hip-fracture':'sec_hip','tkr':'sec_knee','knee-arthroscopy':'sec_sport','rotator-cuff':'sec_fx','ankle-fracture':'sec_sport','amputation':'sec_sport','laminectomy':'sec_spine','fusion-discectomy':'sec_spine','kyphoplasty':'sec_spine','oxygen-sleep':'sec_after','enoxaparin-injections':'sec_home','preop':'sec_preop'};
var f=OWN.indexOf(pg)>=0?'p/'+pg:SEC[pg];if(!f)return;
var u='../media/img/'+f+'.webp';
document.body.style.setProperty('--ph','url("'+new URL(u,location.href).href+'")');document.body.classList.add('hasph');
var h=document.querySelector('header');if(h)h.classList.add('ph');
document.querySelectorAll('main>[data-l]').forEach(function(d){var fig=document.createElement('div');fig.className='phero';fig.innerHTML='<img src="'+u+'" alt="" width="1200" height="800" decoding="async">';d.prepend(fig)});
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});document.querySelectorAll('main section').forEach(function(s){s.classList.add('rv');io.observe(s)})}
})();
