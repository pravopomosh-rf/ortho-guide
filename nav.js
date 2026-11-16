/* 16.11: меню на каждой странице + умный поиск по всему сайту (синонимы, опечатки, заголовки внутри страниц) + голосовой поиск.
   Данные — nav-data.js (строит tools/mknav.py). Без сбора данных; голос распознаёт браузер/телефон пользователя. */
(function(){
var B=/\/ops\//.test(location.pathname)?'../':'';window.NAVD=window.NAVD||{};var LD={};
function need(l,cb,fail){if(NAVD[l])return cb();if(!LD[l]){LD[l]=[];var sc=document.createElement('script');sc.src=B+'nav-'+l+'.js?v=1611n';sc.onload=function(){var q=LD[l];LD[l]=0;q.forEach(function(f){f[0]()})};sc.onerror=function(){var q=LD[l];LD[l]=null;sc.remove();q.forEach(function(f){if(f[1])f[1]()})};document.head.appendChild(sc)}if(LD[l])LD[l].push([cb,fail])}
var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
var TX={
ru:{menu:'Меню',bar:'Поиск по сайту',ph:'Что ищете? Колено, уколы, падение…',home:'Главная',map:'Карта сайта',close:'Закрыть',mic:'Сказать голосом',lis:'Говорите…',none:'Точного совпадения нет. Посмотрите разделы:',near:'Похожие темы',vid:'видео',path:'по шагам',in:'найдено:',secs:'Разделы',voice:'ru-RU',dir:'ltr',load:'Загрузка…',neterr:'Нет связи с сайтом. Проверьте интернет и нажмите здесь, чтобы повторить.',pop:'Часто ищут',popw:['Колено','Бедро','Плечо','Позвоночник','Уколы','Падение','Боль','Повязка'],vno:'В этом браузере голосовой поиск не работает. Нажмите значок микрофона на клавиатуре телефона и скажите, что ищете.',vden:'Нет доступа к микрофону. Разрешите микрофон для этого сайта в настройках браузера или нажмите микрофон на клавиатуре телефона.',vnos:'Не расслышали. Нажмите микрофон ещё раз и говорите.'},
he:{menu:'תפריט',bar:'חיפוש באתר',ph:'מה מחפשים? ברך, זריקות, נפילה…',home:'דף הבית',map:'מפת האתר',close:'סגירה',mic:'חיפוש קולי',lis:'דברו עכשיו…',none:'לא נמצאה התאמה מדויקת. עיינו בנושאים:',near:'נושאים קרובים',vid:'סרטון',path:'שלב אחר שלב',in:'נמצא:',secs:'נושאים',voice:'he-IL',dir:'rtl',load:'טוען…',neterr:'אין חיבור לאתר. בדקו את האינטרנט ולחצו כאן כדי לנסות שוב.',pop:'חיפושים נפוצים',popw:['ברך','ירך','כתף','עמוד שדרה','זריקות','נפילה','כאב','חבישה'],vno:'בדפדפן הזה חיפוש קולי לא עובד. לחצו על סמל המיקרופון במקלדת הטלפון ואמרו מה אתם מחפשים.',vden:'אין גישה למיקרופון. אפשרו את המיקרופון לאתר בהגדרות הדפדפן או לחצו על המיקרופון במקלדת הטלפון.',vnos:'לא שמענו. לחצו שוב על המיקרופון ודברו.'},
ar:{menu:'القائمة',bar:'البحث في الموقع',ph:'ابحثوا: الركبة، الحقن، السقوط…',home:'الصفحة الرئيسية',map:'خريطة الموقع',close:'إغلاق',mic:'البحث بالصوت',lis:'تحدّثوا الآن…',none:'لا توجد نتيجة مطابقة تمامًا. تصفّحوا الأقسام:',near:'مواضيع قريبة',vid:'فيديو',path:'خطوة بخطوة',in:'وُجد:',secs:'الأقسام',voice:'ar-SA',dir:'rtl',load:'جارٍ التحميل…',neterr:'لا يوجد اتصال بالموقع. تحقّقوا من الإنترنت واضغطوا هنا للمحاولة مرة أخرى.',pop:'عمليات بحث شائعة',popw:['الركبة','الورك','الكتف','العمود الفقري','الحقن','السقوط','الألم','الضماد'],vno:'البحث الصوتي لا يعمل في هذا المتصفح. اضغطوا على رمز الميكروفون في لوحة مفاتيح الهاتف وقولوا ما تبحثون عنه.',vden:'لا يوجد إذن للميكروفون. اسمحوا باستخدام الميكروفون لهذا الموقع في إعدادات المتصفح أو اضغطوا على الميكروفون في لوحة مفاتيح الهاتف.',vnos:'لم نسمعكم. اضغطوا على الميكروفون مرة أخرى وتحدّثوا.'},
en:{menu:'Menu',bar:'Search the site',ph:'Search: knee, injections, falls…',home:'Home',map:'Site map',close:'Close',mic:'Search by voice',lis:'Speak now…',none:'No exact match. Browse the sections:',near:'Related topics',vid:'video',path:'step by step',in:'found:',secs:'Sections',voice:'en-GB',dir:'ltr',load:'Loading…',neterr:'No connection to the site. Check your internet and tap here to try again.',pop:'Popular searches',popw:['Knee','Hip','Shoulder','Spine','Injections','Falls','Pain','Dressing'],vno:'Voice search does not work in this browser. Tap the microphone on your phone keyboard and say what you are looking for.',vden:'No microphone access. Allow the microphone for this site in your browser settings, or tap the microphone on your phone keyboard.',vnos:'We did not hear you. Tap the microphone again and speak.'}};
function lang(){var c=document.body.className.split(' ')[0];return TX[c]?c:(c=='am'?'en':'he')}
function norm(s){return (s||'').toLowerCase().replace(/ё/g,'е').replace(/[֑-ׇً-ٰٟـ]/g,'').replace(/[إأآٱ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/[^\p{L}\p{N}]+/gu,' ').trim()}
function stem(w){return w.length>=6?w.slice(0,w.length-2):(w.length==5?w.slice(0,4):w)}
/* приставки иврита/арабского: ה ו ב ל מ ש כ / ال و ب ل ف */
function strip(w,l){var o=[w];if(l=='he'){var x=w;for(var i=0;i<2&&x.length>3&&'הובלמשכ'.indexOf(x[0])>=0;i++){x=x.slice(1);o.push(x)}}
 if(l=='ar'){var y=w;if(y.length>4&&/^[وفبل]/.test(y)){y=y.slice(1);o.push(y)}if(y.length>4&&y.indexOf('ال')==0)o.push(y.slice(2));if(y.length>4&&y.indexOf('لل')==0)o.push(y.slice(2))}return o}
var STOP={ru:'в во на и или с со по при после до для как что у о об от к не ни мне меня мой моя если это ли же бы где когда можно нужно',en:'the a an of in on at after before for my me how to and or with is are i do can what when where',he:'של את עם אחרי לפני איך מה על אם זה יש לי אני מתי איפה או',ar:'في من على بعد قبل كيف ما مع عن الى إلى هل لي انا متى اين او'};
/* синонимы: слова пациента → слова в названиях и заголовках страниц */
var SY={
ru:[['bedsor','bed sor','pressure sor','pressure ulc','пролежн'],['пролежн','pressure'],['паден','упад','упал','упаст','пада','равновес','головокруж','спотк','поскольз'],['упаст','паден','ходунк'],
 ['плеч','рук'],['плеч','манжет'],['артроскоп','эндоскоп'],['артроскоп'],['колен','мениск','связк'],['колен'],
 ['бедр','тазобедр','тбс','таз'],['тазобедр','бедр'],['протез','эндопротез','замен','искусствен'],['замен','эндопротез'],
 ['позвон','спин','поясниц','грыж','шея','шеи','шейн','диск','радикул','ишиас','позвоноч'],['позвоноч','ламинэктом','спондилодез','дискэктом','кифопласт'],
 ['перелом','слома','слом','трещин'],['перелом','остеосинтез'],['укол','инъекц','клексан','крусия','тромб','разжиж','эноксапарин'],['укол','эноксапарин','тромб'],
 ['ран','шов','швы','перевяз','повязк','заживл','мокнет'],['перевяз','ран'],['бол','болит','обезбол','анальг'],['боль','боли','болев','обезбол'],['отек','отеч','опух','отекл'],['отек','отёк'],
 ['пролеж'],['пролежн'],['дыхан','дыша','кашл','легк','одышк'],['дыхат','дыхан'],['кислород','сатурац','храп','апноэ'],['кислород','сатурац'],
 ['наркоз','анестез','горло','сонлив','тошн'],['наркоз','анестез'],['спутан','делир','бред','память','путает','галлюц'],['спутан','делир'],
 ['дренаж','трубк'],['дренаж'],['выписк','домой','дома'],['выписк','дома'],['ходунк','костыл','трост','ходьб','ходит'],['ходунк'],
 ['реабил','шикум','физиотер','упражн','лфк','восстановл'],['реабилит','восстановл','упражн'],['подготов','перед операц','анализ'],['подготов'],
 ['поступл','госпитал','прием','кабал','приём','госпитализ'],['поступл'],['мазок','бактер','мазк','cpe','vre','изоляц'],['мазок','cpe'],
 ['гной','абсцесс','флегмон','нагно','инфекц','воспал','покрасн','температ','жар'],['гнойн','инфекц','тревожн','целлюлит'],['диабет','сахар'],['диабет'],
 ['ахилл','пятк','сухожил'],['ахилл'],['лодыж','голеност','стоп','голен','нога','ноги'],['лодыж','голен','стоп'],['запяст','кист','лучев'],['запяст'],
 ['ампутац'],['ампутац'],['кроват','встат','встава','подня','поворач'],['встава','кроват'],['ждат','тянут','терпет','годами'],['годами','без помощи']],
en:[['bedsor','bed sor','pressure sor','pressure ulc'],['pressure'],['fall','fell','balance','dizzy','trip','slip'],['fall','walker'],['shoulder','arm'],['shoulder','cuff'],['arthroscop','keyhole','scope'],['arthroscop'],
 ['knee','menisc','ligament'],['knee'],['hip','pelvi'],['hip'],['replace','prosthe','implant','artificial','joint'],['replacement'],
 ['spine','spinal','back','neck','disc','hernia','sciatica','vertebr','lumbar'],['spine','spinal','laminectomy','fusion','kyphoplasty'],
 ['fractur','broke','break','crack'],['fracture','osteosynthesis'],['inject','shot','clexane','clot','thinner','enoxaparin','dvt'],['injection','enoxaparin','clot'],
 ['wound','stitch','suture','dressing','bandage','scar','healing'],['wound','dressing'],['pain','hurt','ache','painkill'],['pain'],['swell','swollen','oedema','edema'],['swelling'],
 ['pressure','bedsore','sore'],['pressure'],['breath','cough','lung'],['breath'],['oxygen','saturat','snor','apnea','apnoea'],['oxygen','saturation'],
 ['anaesth','anesth','throat','sleepy','nausea'],['anaesthe'],['confus','delirium','memory','halluc'],['confusion','delirium'],['drain','tube'],['drain'],
 ['discharg','home'],['discharge','home'],['walker','crutch','cane','stick','walking','frame'],['walker'],['rehab','physio','exercis','recover'],['rehab','exercise','recovery'],
 ['prepar','before'],['prepar'],['admission','admit','arriv'],['admission'],['swab','bacteri','cpe','vre','isolat'],['swab','cpe'],
 ['pus','abscess','infect','redness','fever','cellulit'],['infection','purulent','warning','cellulitis'],['diabet','sugar'],['diabet'],['achilles','heel','tendon'],['achilles'],
 ['ankle','foot','leg','shin'],['ankle','foot','leg'],['wrist','hand','radius'],['wrist'],['amput'],['amputation'],['bed','get up','getting up','roll'],['bed','getting'],['wait','delay','years'],['years','wait']],
he:[['פצעי לחץ','פצע לחץ'],['לחץ'],['נפיל','ליפול','נפל','שיווי','סחרחור','החלק','מעד'],['ליפול','נפיל','הליכון'],['כתף','זרוע','יד'],['כתף','השרוול'],['ארתרוסקופ','סקופי'],['ארתרוסקופ'],
 ['ברך','מניסק','רצוע'],['ברך'],['ירך','אגן','מפרק הירך'],['ירך'],['החלפ','תותב','פרוטז','מפרק מלאכותי'],['החלפ','תותב'],
 ['גב','עמוד השדרה','צוואר','דיסק','פריצ','סיאטיק','חוליה','חוליות'],['עמוד השדרה','למינקטומי','קיבוע','קיפופלסטי'],['שבר','נשבר','סדק'],['שבר','קיבוע'],
 ['זריק','קלקסן','קרישי','קריש','מדלל','אנוקספרין','פקקת'],['זריק','אנוקספרין','קריש'],['פצע','תפר','חביש','צלקת','החלמ'],['חביש','פצע'],['כאב','כואב','משכך'],['כאב'],
 ['נפיח','בצק','נפוח'],['נפיח','בצק'],['פצעי לחץ','לחץ'],['לחץ'],['נשימ','שיעול','ריאות'],['נשימ'],['חמצן','ריווי','סטורצי','נחירות','דום נשימה'],['חמצן','ריווי'],
 ['הרדמ','נרקוז','גרון','ישנוני','בחיל'],['הרדמ'],['בלבול','דליריום','זיכרון','הזי'],['בלבול','דליריום'],['נקז','צינור'],['נקז'],['שחרור','בית','הביתה'],['שחרור','בבית'],
 ['הליכון','קביים','מקל','הליכה'],['הליכון'],['שיקום','פיזיותרפי','תרגיל','החלמה'],['שיקום','תרגיל'],['הכנ','לפני הניתוח'],['הכנ'],['קבל','אשפוז','התקבל'],['קבל'],
 ['משטח','חיידק','בידוד'],['משטח','חיידק'],['מוגל','מורסה','אבצס','זיהום','אדמומי','חום'],['זיהום','מוגל','סימני אזהרה'],['סוכרת','סוכר'],['סוכרת'],['אכילס','עקב','גיד'],['אכילס'],
 ['קרסול','כף רגל','רגל','שוק'],['קרסול','שוק','כף הרגל'],['שורש','כף היד','רדיוס'],['שורש כף היד'],['קטיע'],['קטיע'],['מיטה','לקום','קימה','להתהפך'],['מיטה','לקום'],['לחכות','שנים'],['שנים']],
ar:[['قرح الفراش','قرحه الفراش','تقرحات الفراش'],['قرح'],['منظار','تنظير'],['تنظير','منظار'],['سقوط','سقط','اسقط','وقوع','توازن','دوخه','دوار','انزلاق'],['السقوط','تسقطوا','المشايه'],['كتف','ذراع','يد'],['الكتف','الكفه'],['منظار'],['منظار'],
 ['ركبه','ركب','غضروف','رباط'],['الركبه'],['ورك','حوض'],['الورك'],['استبدال','مفصل صناعي','بديل'],['استبدال'],
 ['ظهر','العمود','فقري','رقبه','ديسك','انزلاق غضروفي','عرق النسا','فقره'],['الفقري','الفقرات'],['كسر','انكسر','شرخ'],['كسر'],
 ['حقن','ابره','ابر','كليكسان','جلطه','جلطات','مميع','انوكسابارين'],['حقن','انوكسابارين','الجلطات'],['جرح','غرز','ضماده','ضماد','ندبه','التئام'],['ضماد','الجرح'],['الم','وجع','مسكن'],['الالم'],
 ['تورم','انتفاخ','وذمه'],['تورم'],['قرح','تقرح','فراش'],['قرح'],['تنفس','سعال','رئه','رئتين'],['التنفس'],['اكسجين','تشبع','شخير'],['الاكسجين','تشبع'],
 ['تخدير','بنج','حلق','نعاس','غثيان'],['التخدير'],['ارتباك','هذيان','ذاكره','هلوس'],['الارتباك','الهذيان'],['تصريف','انبوب','درنقه'],['التصريف','نزح'],
 ['خروج','البيت','المنزل'],['الخروج','البيت'],['مشايه','عكاز','عصا','مشي'],['المشايه'],['تاهيل','علاج طبيعي','تمارين','تعافي'],['التاهيل','تمارين'],['تحضير','قبل العمليه'],['التحضير'],
 ['دخول','قبول','استقبال'],['الدخول'],['مسحه','بكتيريا','عزل'],['مسحه','البكتيريا'],['صديد','قيح','خراج','عدوى','احمرار','حمى','حراره'],['العدوى','قيحيه','علامات'],['سكري','سكر'],['السكري'],
 ['اخيل','كعب','وتر'],['اخيل'],['كاحل','قدم','ساق','رجل'],['الكاحل','القدم','الساق'],['معصم','رسغ','كف'],['الرسغ','المعصم'],['بتر'],['بتر'],['سرير','نهوض','القيام'],['السرير','النهوض'],['انتظار','سنوات'],['سنوات']]};
var CACHE={};
function data(l){if(CACHE[l])return CACHE[l];var d=NAVD[l];var docs=d.docs.map(function(e,i){
 function ws(s){var a=[];norm(s).split(' ').forEach(function(w){if(w)strip(w,l).forEach(function(x){a.push(x)})});return a}
 var heads=e.k?e.k.split(' | '):[];
 return {e:e,i:i,f:[{w:ws(e.t),s:' '+norm(e.t)+' ',k:5},{w:ws(e.s),s:' '+norm(e.s)+' ',k:2},{w:ws(e.k),s:' '+norm(e.k)+' ',k:1},{w:ws(e.b),s:'',k:.6,b:1}],heads:heads.map(function(h){return {h:h,n:' '+norm(h)+' '}})}});
 var sy=(SY[l]||[]).map(function(x){return x.map(norm)});var pairs=[];for(var j=0;j+1<sy.length;j+=2)pairs.push([sy[j],sy[j+1]]);
 return CACHE[l]={d:d,docs:docs,sy:pairs,stop:' '+(STOP[l]||'')+' '}}
function lev(a,b){if(Math.abs(a.length-b.length)>2)return 9;var p=[],i,j;for(j=0;j<=b.length;j++)p[j]=j;for(i=1;i<=a.length;i++){var q=[i];for(j=1;j<=b.length;j++)q[j]=Math.min(p[j]+1,q[j-1]+1,p[j-1]+(a[i-1]==b[j-1]?0:1));p=q}return p[b.length]}
function wm(fw,s,syn){return syn&&s.length<=4?(fw.indexOf(s)==0&&fw.length<=s.length+1):(s.length<=3?(fw.indexOf(s)==0&&fw.length<=4):fw.indexOf(s)==0)}
function search(q,l){var D=data(l);q=norm(q);if(q.length<2)return null;
 var words=q.split(' ').filter(function(w){return w.length>1&&D.stop.indexOf(' '+w+' ')<0});if(!words.length)words=q.split(' ');
 var P=[];D.sy.forEach(function(p){if(p[0].some(function(k){return k.indexOf(' ')>=0&&q.indexOf(k)>=0}))P=P.concat(p[1])});
 var W=words.map(function(w){var v=[];strip(w,l).forEach(function(x){v.push(stem(x))});var syn=[];
  D.sy.forEach(function(p){if(p[0].some(function(k){return k.indexOf(' ')<0&&v.some(function(s){return s.indexOf(k)==0||(s.length>=4&&k.indexOf(s)==0)})}))syn=syn.concat(p[1])});
  return {w:w,v:v,syn:syn}});
 if(P.length)W.push({w:'',v:[],syn:P,ph:1});
 function hm(x,f){var m=0;
  x.v.forEach(function(s){if(f.w.some(function(fw){return wm(fw,s)}))m=1});
  if(m<1)x.syn.forEach(function(s){if(s.indexOf(' ')>=0?f.s.indexOf(' '+s)>=0:f.w.some(function(fw){return wm(fw,s,1)}))m=Math.max(m,x.ph?1.5:.8)});
  if(m<.5&&!f.b&&x.w.length>=5)x.v.forEach(function(s){var t=s.length>=7?2:1;if(s.length<5)return;if(f.w.some(function(fw){return fw.length>=s.length-1&&lev(s,fw.slice(0,s.length))<=t}))m=Math.max(m,.5)});
  return m}
 var res=D.docs.map(function(o){var sc=0,hit=0,why=null,phr=0;
  W.forEach(function(x){var best=0,bh=0;
   o.f.forEach(function(f){var m=hm(x,f);if(m*f.k>best){best=m*f.k;bh=f.k==1}});
   if(best>0){if(!x.ph)hit++;else phr=1;sc+=best;if(bh&&!why)why=x}});
  if(!hit&&!sc)return null;var nw=W.filter(function(x){return !x.ph}).length;if(hit==nw||phr)sc*=1.6;
  var head='';if(why){for(var i=0;i<o.heads.length&&!head;i++){var hf={w:o.heads[i].n.trim().split(' ').reduce(function(a,w){return a.concat(strip(w,l))},[]),s:o.heads[i].n};if(hm(why,hf)>=.8)head=o.heads[i].h}}
  return {o:o,sc:sc+(o.e.v?.2:0),head:head}}).filter(Boolean).sort(function(a,b){return b.sc-a.sc||a.o.i-b.o.i});
 var top=res.length?res[0].sc:0;res=res.filter(function(r){return r.sc>=top*.35}).slice(0,12);
 /* мало результатов — добавить соседние темы из тех же разделов */
 if(res.length&&res.length<4){var have={};res.forEach(function(r){have[r.o.e.h]=1});var rel=[];
  D.d.secs.forEach(function(sc){if(sc.items.some(function(i){return have[i.h]}))sc.items.forEach(function(i){if(!have[i.h]&&!i.p){have[i.h]=1;var o=D.docs.filter(function(d){return d.e.h==i.h})[0];if(o)rel.push({o:o,sc:0,head:'',rel:1})}})});
  res=res.concat(rel.slice(0,5))}
 return res}
/* ——— стили ——— */
var css='.gnav{position:sticky;top:0;z-index:60;display:flex;gap:8px;align-items:center;padding:8px 12px;background:rgba(251,247,240,.92);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-bottom:1px solid var(--line,#e6ded0)}'+
'.gnav{gap:12px!important;padding:10px 12px!important;background:#fbf7f0!important;box-shadow:0 2px 10px rgba(40,60,55,.08)}.gnav button{font:inherit;cursor:pointer;border:0}'+
'.gsb{flex:1;min-width:0;display:flex;align-items:center;background:#fff;border:2px solid var(--line,#e6ded0);border-radius:999px;padding:2px 3px 2px 0}[dir=rtl] .gsb{padding:2px 0 2px 3px}.gsb .gns{border:0!important;background:none;padding:9px 12px}.gsb .gmic{width:40px;height:40px}.gnt{overflow:hidden;text-overflow:ellipsis}'+
'.gnb{display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:14px;background:var(--teal,#1f7a70);color:#fff;font-size:16px;font-weight:600;white-space:nowrap}'+
'.gnb i{display:block;width:18px;height:12px;border-top:2px solid #fff;border-bottom:2px solid #fff;position:relative}.gnb i::after{content:"";position:absolute;left:0;right:0;top:3px;border-top:2px solid #fff}'+
'.gns{flex:1;min-width:0;display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:14px;background:#fff;color:var(--ink2,#46595a);font-size:16px;text-align:start;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}'+
'.gico{flex:none;width:18px;height:18px;border:2.5px solid currentColor;border-radius:50%;position:relative;margin-inline-end:2px}.gico::after{content:"";position:absolute;width:8px;border-top:2.5px solid currentColor;right:-6px;bottom:-3px;transform:rotate(45deg)}'+
'.gmic{flex:none;width:44px;height:44px;border-radius:50%;background:var(--teal-l,#e3f2ee);color:var(--teal-d,#14564f);display:flex;align-items:center;justify-content:center}'+
'.gmic svg{width:22px;height:22px}.gmic.on{background:#e98a6e;color:#fff;animation:gpul 1.2s infinite}@keyframes gpul{50%{box-shadow:0 0 0 10px rgba(233,138,110,.25)}}'+
'.gov{position:fixed;inset:0;z-index:100;background:var(--bg,#fbf7f0);display:flex;flex-direction:column;animation:gin .18s ease-out}@keyframes gin{from{opacity:0;transform:translateY(12px)}}'+
'.goh{display:flex;gap:8px;align-items:center;padding:12px;border-bottom:1px solid var(--line,#e6ded0);background:#fff}'+
'.gsf{flex:1;min-width:0;display:flex;align-items:center;gap:8px;padding:0 4px 0 14px;border:2px solid var(--teal,#1f7a70);border-radius:999px;background:#fff;color:var(--ink2,#46595a)}[dir=rtl] .gsf{padding:0 14px 0 4px}.gsf:focus-within{box-shadow:0 0 0 3px var(--teal-l,#e3f2ee)}.gsf .gmic{width:40px;height:40px}'+
'.goh input{flex:1;min-width:0;font:inherit;font-size:18px;padding:11px 0;border:0;background:none;color:var(--ink,#1d2b2a)}.goh input:focus{outline:none}.gtt{flex:1;font-size:20px;padding:0 4px}.gm .goh{background:var(--teal,#1f7a70);color:#fff}.gm .gtt{color:#fff}.gm .gx{background:rgba(255,255,255,.18);color:#fff}.gerr{cursor:pointer;text-decoration:underline}'+
'.gx{flex:none;width:44px;height:44px;border-radius:50%;border:0;background:var(--bg2,#f3efe6);font-size:22px;line-height:1;color:var(--ink,#1d2b2a);cursor:pointer}'+
'.gob{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:12px 12px 40px}.gob h3{margin:14px 4px 8px;font-size:15px;color:var(--ink2,#46595a);font-weight:600;letter-spacing:.02em}'+
'.gql{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 10px}.gql a{padding:9px 14px;border-radius:999px;background:#fff;border:1px solid var(--line,#e6ded0);color:var(--teal-d,#14564f);text-decoration:none;font-weight:600;font-size:15px}'+
'.gsec{background:#fff;border-radius:18px;margin:0 0 10px;box-shadow:0 1px 4px rgba(40,60,55,.06);overflow:hidden}.gsec summary{list-style:none;display:flex;align-items:center;gap:12px;padding:10px 12px;cursor:pointer;font-weight:700;font-size:17px}'+
'.gsec summary::-webkit-details-marker{display:none}.gsec summary img{width:56px;height:40px;object-fit:cover;border-radius:10px;flex:none}.gsec summary span{flex:1}.gsec summary b{flex:none;color:var(--teal,#1f7a70);transition:transform .2s}.gsec[open] summary b{transform:rotate(90deg)}'+
'.gsec ul,.gres{list-style:none;margin:0;padding:0}.gsec li a,.gres a{display:block;padding:11px 14px;border-top:1px solid var(--line,#e6ded0);color:var(--ink,#1d2b2a);text-decoration:none;font-size:16px;line-height:1.35}'+
'.gres{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 1px 4px rgba(40,60,55,.06)}.gres li:first-child a{border-top:0}.gres b{display:block;font-size:17px}.gres small{display:block;color:var(--ink2,#46595a);font-size:14px;margin-top:2px}'+
'.gsec li a:active,.gres a:active,.gsec li a:hover,.gres a:hover{background:var(--teal-l,#e3f2ee)}.gtag{display:inline-block;margin-inline-start:6px;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:700;vertical-align:2px;background:var(--dawn-l,#fff3e3);color:#9a5a12}.gtag.p{background:var(--teal-l,#e3f2ee);color:var(--teal-d,#14564f)}'+
'.gnone{margin:6px 4px 12px;color:var(--ink2,#46595a)}.glis{margin:8px 12px 0;padding:10px 12px;border-radius:12px;background:#fff3e3;color:#9a4a20;font-weight:600;line-height:1.4}body.gopen{overflow:hidden}'+
'.srch .gmic{position:absolute;inset-inline-end:6px;top:50%;transform:translateY(-50%)}.srch .srl{position:relative}.srch input{padding-inline-end:58px!important}'+
'@media print{.gnav,.gov{display:none!important}}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
var MIC='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function link(h,l){return B+h+'#lang='+l}
function tags(e,t){return (e.p?'<span class="gtag p">'+t.path+'</span>':'')+(e.v?'<span class="gtag">▶ '+t.vid+'</span>':'')}
function resHTML(r,l,t){var a=r.filter(function(x){return !x.rel}),b=r.filter(function(x){return x.rel});return li(a,l,t)+(b.length?'<h3>'+t.near+'</h3>'+li(b,l,t):'')}
function li(r,l,t){return '<ul class="gres">'+r.map(function(x){var e=x.o.e;return '<li><a href="'+link(e.h,l)+'"><b>'+esc(e.t)+tags(e,t)+'</b><small>'+esc(e.s)+(x.head?' · '+t.in+' «'+esc(x.head)+'»':'')+'</small></a></li>'}).join('')+'</ul>'}
function menuHTML(l,t){var d=data(l).d;return '<div class="gql"><a href="'+B+'index.html#lang='+l+'">⌂ '+t.home+'</a><a href="'+B+'ops/sitemap.html#lang='+l+'">'+t.map+'</a></div><h3>'+t.secs+'</h3>'+
 d.secs.map(function(s){var here=s.items.some(function(i){return location.pathname.slice(-i.h.length-1)=='/'+i.h});
  return '<details class="gsec"'+(here?' open':'')+'><summary>'+(s.i?'<img src="'+B+s.i+'" alt="" loading="lazy">':'')+'<span>'+esc(s.t)+'</span><b>›</b></summary><ul>'+
  s.items.map(function(i){return '<li><a href="'+link(i.h,l)+'">'+esc(i.t)+tags(i,t)+'</a></li>'}).join('')+'</ul></details>'}).join('')}
function fill(box,q,l,t,full){var r=search(q,l);
 if(r===null){box.innerHTML=full?menuHTML(l,t):'';return}
 if(r.length){box.innerHTML=resHTML(r,l,t)+(full?'':'');return}
 box.innerHTML='<p class="gnone">'+t.none+'</p>'+(full?menuHTML(l,t).replace(/^<div class="gql">.*?<\/div><h3>.*?<\/h3>/,''):'')}
function voice(btn,inp,l,t,status){btn.title=t.mic;btn.setAttribute('aria-label',t.mic);
 function msg(x){if(status)status(x)}
 btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();if(btn._r){try{btn._r.stop()}catch(_){}return}
  if(!SR){msg(t.vno);inp.focus();return}
  var r;try{r=new SR()}catch(_){msg(t.vno);inp.focus();return}
  r.lang=TX[lang()].voice;r.interimResults=true;r.maxAlternatives=1;r.continuous=false;btn._r=r;btn.classList.add('on');msg(t.lis);var got=0,err='';
  var to=setTimeout(function(){try{r.stop()}catch(_){}},12000);
  r.onresult=function(ev){var s2='';for(var i=0;i<ev.results.length;i++)s2+=ev.results[i][0].transcript;got=1;inp.value=s2;inp.dispatchEvent(new Event('input'))};
  r.onerror=function(ev){err=ev&&ev.error||'x'};
  r.onend=function(){clearTimeout(to);btn.classList.remove('on');btn._r=null;
   if(got)msg('');else if(err=='not-allowed'||err=='service-not-allowed')msg(t.vden);else if(err=='no-speech'||err=='aborted'||!err)msg(t.vnos);else{msg(t.vno);inp.focus()}};
  try{r.start()}catch(_){clearTimeout(to);btn.classList.remove('on');btn._r=null;msg(t.vno);inp.focus()}})}
/* ——— полноэкранное меню + поиск ——— */
var ov=null;
function load(box,l,t,cb){if(NAVD[l])return cb();box.innerHTML='<p class="gnone">'+t.load+'</p>';
 need(l,function(){if(box.isConnected)cb()},function(){if(!box.isConnected)return;box.innerHTML='<p class="gnone gerr">'+t.neterr+'</p>';box.querySelector('.gerr').onclick=function(){load(box,l,t,cb)}})}
function pop(box,inp,t){box.innerHTML='<h3>'+t.pop+'</h3><div class="gql">'+t.popw.map(function(w){return '<a href="#" data-q="'+esc(w)+'">'+esc(w)+'</a>'}).join('')+'</div>';
 box.querySelectorAll('[data-q]').forEach(function(a){a.onclick=function(e){e.preventDefault();inp.value=a.getAttribute('data-q');inp.dispatchEvent(new Event('input'))}})}
function open(mode){var l=lang(),t=TX[l];if(ov)close();var menu=!mode;
 ov=document.createElement('div');ov.className='gov'+(menu?' gm':' gs');ov.setAttribute('role','dialog');ov.setAttribute('aria-modal','true');ov.setAttribute('aria-label',menu?t.menu:t.bar);ov.dir=t.dir;ov.lang=l;
 ov.innerHTML='<div class="goh">'+(menu?'<b class="gtt">'+esc(t.menu)+'</b>':'<div class="gsf"><span class="gico" aria-hidden="true"></span><input type="search" enterkeyhint="search" autocomplete="off" placeholder="'+esc(t.ph)+'" aria-label="'+esc(t.bar)+'"><button type="button" class="gmic">'+MIC+'</button></div>')+'<button type="button" class="gx" aria-label="'+esc(t.close)+'">✕</button></div><div class="gob"></div>';
 document.body.appendChild(ov);document.body.classList.add('gopen');
 var box=ov.querySelector('.gob'),inp=ov.querySelector('input');
 if(menu){load(box,l,t,function(){box.innerHTML=menuHTML(l,t)})}
 else{var st=function(x){var p=ov&&ov.querySelector('.glis');if(x){if(!p){p=document.createElement('p');p.className='glis';box.parentNode.insertBefore(p,box)}p.textContent=x}else if(p)p.remove()};
  var run=function(){if(!inp.value.trim()){pop(box,inp,t);return}load(box,l,t,function(){fill(box,inp.value,l,t,1)})};
  inp.addEventListener('input',run);run();need(l,function(){});voice(ov.querySelector('.gmic'),inp,l,t,st)}
 /* ссылка внутри — закрыть окно (иначе переход по #якорю на той же странице оставляет его открытым) */
 ov.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(a&&a.getAttribute('href')!='#'){close();try{if(history.state&&history.state.gnav)history.replaceState(null,'')}catch(_){}}});
 ov.querySelector('.gx').addEventListener('click',function(){history.state&&history.state.gnav?history.back():close()});
 ov.addEventListener('keydown',function(e){if(e.key=='Escape')ov.querySelector('.gx').click()});
 try{history.pushState({gnav:1},'')}catch(_){}
 if(mode=='mic'){ov.querySelector('.gmic').click()}else if(inp)inp.focus()}
function close(){if(!ov)return;ov.remove();ov=null;document.body.classList.remove('gopen')}
window.addEventListener('popstate',function(){if(ov)close()});
function bar(){var l=lang(),t=TX[l];var b=document.querySelector('.gnav');if(!b){b=document.createElement('div');b.className='gnav';document.body.insertBefore(b,document.body.firstChild)}
 b._l=l;b.dir=t.dir;b.innerHTML='<button type="button" class="gnb" aria-haspopup="dialog"><i aria-hidden="true"></i>'+t.menu+'</button><div class="gsb"><button type="button" class="gns"><span class="gico" aria-hidden="true"></span><span class="gnt">'+t.bar+'</span></button><button type="button" class="gmic" aria-label="'+esc(t.mic)+'" title="'+esc(t.mic)+'">'+MIC+'</button></div>';
 b.querySelector('.gnb').onclick=function(){open(0)};b.querySelector('.gns').onclick=function(){open(1)};b.querySelector('.gmic').onclick=function(){open('mic')}}
/* ——— поиск прямо на главной (заменяет старый search.js) ——— */
function inline(){document.querySelectorAll('.cards[id^="top_"]').forEach(function(box){var l=box.id.slice(4),t=TX[l];if(!t||box.querySelector('.srch'))return;
 var w=document.createElement('div');w.className='srch';
 w.innerHTML='<label class="srl"><span class="vh">'+t.bar+'</span><input type="search" enterkeyhint="search" autocomplete="off" placeholder="'+esc(t.ph)+'">'+'<button type="button" class="gmic">'+MIC+'</button></label><div class="srbox"></div>';
 var h=box.querySelector('.hint')||box.querySelector('.cardsh');if(h)h.insertAdjacentElement('afterend',w);else box.prepend(w);
 var inp=w.querySelector('input'),res=w.querySelector('.srbox');res.style.marginTop='8px';
 inp.addEventListener('focus',function(){need(l,function(){})});inp.addEventListener('input',function(){need(l,function(){fill(res,inp.value,l,t,0)})});var m=w.querySelector('.gmic');if(m)voice(m,inp,l,t,function(x){var p=w.querySelector('.glis');if(x){if(!p){p=document.createElement('p');p.className='glis';res.parentNode.insertBefore(p,res)}p.textContent=x}else if(p)p.remove()})})}
bar();inline();setTimeout(function(){need(lang(),function(){})},2500);
/* смена языка кнопками страницы → обновить панель */
new MutationObserver(function(){var b=document.querySelector('.gnav');if(b&&b._l!==lang()){b._l=lang();bar()}}).observe(document.body,{attributes:true,attributeFilter:['class']});
window.NAVSEARCH=search;window.NAVNEED=need;
})();
