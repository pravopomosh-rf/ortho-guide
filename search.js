/* 13.11: поиск по темам на главной (только по заголовкам карточек и разделов; без сети, без сбора данных) */
(function(){
var T={ru:{ph:'Поиск: колено, уколы, пролежни…',lb:'Поиск по темам',no:'Ничего не нашлось. Попробуйте другое слово или выберите раздел ниже.'},
he:{ph:'חיפוש: ברך, זריקות, פצעי לחץ…',lb:'חיפוש נושא',no:'לא נמצא. נסו מילה אחרת או בחרו נושא למטה.'},
ar:{ph:'بحث: الركبة، الحقن، قرح الفراش…',lb:'البحث في المواضيع',no:'لا توجد نتائج. جرّبوا كلمة أخرى أو اختاروا قسمًا أدناه.'},
en:{ph:'Search: knee, injections, pressure sores…',lb:'Search topics',no:'Nothing found. Try another word or choose a section below.'}};
function norm(s){return (s||'').toLowerCase().replace(/ё/g,'е').replace(/[\u0591-\u05C7\u064B-\u065F\u0670]/g,'').replace(/[إأآٱ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/[^\p{L}\p{N}]+/gu,' ').trim()}
function stem(w){return w.length>=5?w.slice(0,Math.max(4,w.length-2)):(w.length==4&&/^[а-я]+$/.test(w)?w.slice(0,3):w)}
/* синонимы для навигации: слово запроса → другие слова заголовков */
var SY={'спин':['позвоноч'],'поясниц':['позвоноч'],'шв':['перевяз','ран'],'шов':['перевяз','ран'],'рана':['перевяз','ран'],'тромб':['тромб','эноксапарин'],'back':['spine'],'wound':['dressing','wound'],'stitches':['dressing','wound'],'clot':['clot','enoxaparin'],'גב':['עמוד השדרה'],'תפרים':['חבישה','פצע הניתוח'],'ظهر':['العمود الفقري'],'غرز':['ضماده','جرح']};
document.querySelectorAll('.cards[id^="top_"]').forEach(function(box){
var l=box.id.slice(4),t=T[l];if(!t)return;
var root=box.closest('[data-l]')||document;var seen={},idx=[];
root.querySelectorAll('section.reg').forEach(function(sec){var h=sec.querySelector('.regh');var hs=h?h.textContent:'';
sec.querySelectorAll('a.pc').forEach(function(a){var href=a.getAttribute('href');if(seen[href])return;seen[href]=1;var pt=a.querySelector('.pt'),ch=a.querySelector('.chip');
idx.push({a:a,title:pt?pt.textContent.trim():'',chip:ch?ch.textContent.trim():'',sec:hs.trim(),k:norm((pt?pt.textContent:'')+' '+hs)})})});
if(!idx.length)return;
var w=document.createElement('div');w.className='srch';
w.innerHTML='<label class="srl"><span class="vh">'+t.lb+'</span><input type="search" enterkeyhint="search" autocomplete="off" placeholder="'+t.ph+'"></label><ul class="srr" role="list" hidden></ul><p class="srn" hidden>'+t.no+'</p>';
var h2=box.querySelector('.hint')||box.querySelector('.cardsh');h2.insertAdjacentElement('afterend',w);
var inp=w.querySelector('input'),ul=w.querySelector('.srr'),no=w.querySelector('.srn');
inp.addEventListener('input',function(){var q=norm(inp.value);ul.innerHTML='';if(q.length<2){ul.hidden=true;no.hidden=true;return}
var ws=q.split(' ').filter(function(x){return x.length>1}).map(function(x){var a=[stem(x)];for(var k in SY){if(x.indexOf(k)==0)a=a.concat(SY[k].map(norm))}return a});
var r=idx.filter(function(e){return ws.every(function(a){return a.some(function(x){return e.k.indexOf(x)>=0})})}).map(function(e,i){var tt=' '+norm(e.title);return {e:e,i:i,s:ws.filter(function(a){return a.some(function(x){return tt.indexOf(' '+x)>=0})}).length}}).sort(function(a,b){return b.s-a.s||a.i-b.i}).map(function(o){return o.e}).slice(0,8);
r.forEach(function(e){var li=document.createElement('li');var a=document.createElement('a');a.href=e.a.getAttribute('href');
a.innerHTML='<b></b><small></small>';a.querySelector('b').textContent=e.title;a.querySelector('small').textContent=e.sec+(e.chip?' · '+e.chip:'');li.appendChild(a);ul.appendChild(li)});
ul.hidden=!r.length;no.hidden=!!r.length});
});
})();
