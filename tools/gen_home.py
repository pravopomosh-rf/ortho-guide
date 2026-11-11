import json, re, os, sys
os.chdir(sys.argv[1])
T = json.load(open(sys.argv[2], encoding='utf8'))
s = open('index.html', encoding='utf8').read()
LANGS = ['ru', 'he', 'ar', 'en']

# poster per page (video base name); per-lang availability checked on disk
POSTER = {'amputation': 'amp', 'ankle-fracture': 'ankle', 'knee-arthroscopy': 'arth', 'rotator-cuff': 'cuff',
          'enoxaparin-injections': 'enox', 'fusion-discectomy': 'fusion', 'hip-fracture': 'hipfxv',
          'kyphoplasty': 'kyphoplasty', 'laminectomy': 'laminectomy', 'oxygen-sleep': 'o2',
          'preop': {'ru': 'preopv', 'he': 'preopv', 'ar': 'preop'}, 'thr': 'thr2v', 'thr-anterior': 'stairs', 'tkr': 'tkr'}

def poster(page, L):
    p = POSTER.get(page)
    if isinstance(p, dict): p = p.get(L)
    if not p: return None
    f = 'video/%s_%s.jpg' % (p, L)
    if os.path.exists(f) and os.path.exists('video/%s_%s.mp4' % (p, L)) and ('video/%s_%s.mp4' % (p, L)) in open('ops/%s.html' % page, encoding='utf8').read():
        return f
    return None

SEC = [
 ('preop', 'sec_preop', ['preop', 'why-wait'], None,
  {'ru': 'Подготовка к операции', 'he': 'הכנה לניתוח', 'ar': 'التحضير للعملية', 'en': 'Preparing for surgery'}),
 ('hip', 'sec_hip', ['thr', 'thr-anterior', 'thr-home', 'hip-fracture'], None,
  {'ru': 'Тазобедренный сустав', 'he': 'מפרק הירך', 'ar': 'مفصل الورك', 'en': 'Hip'}),
 ('knee', 'sec_knee', ['tkr', 'knee-arthroscopy'], None,
  {'ru': 'Коленный сустав', 'he': 'מפרק הברך', 'ar': 'مفصل الركبة', 'en': 'Knee'}),
 ('arm', 'p/sec_arm' if os.path.exists('media/img/p/sec_arm.webp') else 'sec_fx', ['rotator-cuff', 'shoulder-replacement', 'shoulder-fracture', 'wrist-fracture', 'osteosynthesis'], None,
  {'ru': 'Плечо и рука', 'he': 'כתף ויד', 'ar': 'الكتف واليد', 'en': 'Shoulder and arm'}),
 ('leg', 'p/sec_leg' if os.path.exists('media/img/p/sec_leg.webp') else 'sec_sport', ['ankle-fracture', 'achilles-repair', 'diabetic-foot', 'amputation', 'osteosynthesis'], None,
  {'ru': 'Голень, лодыжка и стопа', 'he': 'שוק, קרסול וכף רגל', 'ar': 'الساق والكاحل والقدم', 'en': 'Lower leg, ankle and foot'}),
 ('spine', 'sec_spine', ['laminectomy', 'fusion-discectomy', 'kyphoplasty', 'spine-other', 'durotomy', 'log-roll'], None,
  {'ru': 'Позвоночник', 'he': 'עמוד השדרה', 'ar': 'العمود الفقري', 'en': 'Spine'}),
 ('after', 'sec_after', ['after-surgery', 'pain', 'breathing', 'oxygen-sleep', 'falls', 'walker', 'delirium', 'pressure-sores', 'swelling'],
  (['dressings', 'cellulitis', 'purulent-infection', 'cpe-vre'],
   {'ru': 'Рана и инфекции', 'he': 'הפצע וזיהומים', 'ar': 'الجرح والالتهابات', 'en': 'Wound and infections'}),
  {'ru': 'После операции в отделении', 'he': 'אחרי הניתוח במחלקה', 'ar': 'بعد العملية في القسم', 'en': 'After surgery in the ward'}),
 ('home', 'sec_home', ['postop', 'enoxaparin-injections', 'thr-home', 'falls'], None,
  {'ru': 'Выписка и дома', 'he': 'שחרור ובבית', 'ar': 'الخروج والعودة للبيت', 'en': 'Going home'}),
]
UI = {
 'hi': {'ru': 'Здравствуйте! Мы рядом на каждом шаге.', 'he': 'שלום! אנחנו לצדכם בכל שלב.', 'ar': 'أهلًا بكم! نحن معكم في كل خطوة.', 'en': 'Hello! We are with you at every step.'},
 'choose': {'ru': 'Выберите раздел', 'he': 'בחרו נושא', 'ar': 'اختاروا القسم', 'en': 'Choose a section'},
 'hint': {'ru': 'Нажмите на часть тела или тему — откроются памятки и видео.', 'he': 'לחצו על אזור בגוף או על נושא — יופיעו דפי מידע וסרטונים.', 'ar': 'اضغطوا على منطقة في الجسم أو على موضوع — ستظهر صفحات المعلومات والفيديوهات.', 'en': 'Tap a body area or a topic to see information pages and videos.'},
 'ill': {'ru': 'Фотографии — иллюстрации, на них не реальные пациенты.', 'he': 'התמונות להמחשה בלבד ואינן של מטופלים אמיתיים.', 'ar': 'الصور توضيحية فقط وليست لمرضى حقيقيين.', 'en': 'Photos are illustrations, not real patients.'},
 'warn_b': {'ru': 'Тревожные признаки', 'he': 'סימני אזהרה', 'ar': 'علامات الخطر', 'en': 'Warning signs'},
 'warn_s': {'ru': 'Когда звонить 101 или срочно обращаться за помощью', 'he': 'מתי להתקשר ל־101 או לפנות לעזרה דחופה', 'ar': 'متى تتصلون بـ 101 أو تطلبون مساعدة عاجلة', 'en': 'When to call 101 or seek urgent care'},
 'vid': {'ru': '▶ Видео', 'he': '▶ סרטון', 'ar': '▶ فيديو', 'en': '▶ Video'},
 'txt': {'ru': 'Памятка', 'he': 'דף מידע', 'ar': 'صفحة معلومات', 'en': 'Read'},
 'top': {'ru': 'К разделам', 'he': 'לכל הנושאים', 'ar': 'إلى الأقسام', 'en': 'All sections'},
 'map': {'ru': 'Карта сайта: все страницы и видео', 'he': 'מפת האתר: כל הדפים והסרטונים', 'ar': 'خريطة الموقع: كل الصفحات والفيديوهات', 'en': 'Site map: all pages and videos'},
}
# reuse approved wording from the current page for disclaimer and the ward/home note
def grab(L, pat):
    a = s.find('<div data-l="%s"><div class="welcome">' % L)
    b = s.find('<div data-l="%s"><div class="welcome">' % LANGS[LANGS.index(L)+1]) if L != 'en' else s.find('</main>')
    m = re.search(pat, s[a:b], re.S)
    return m.group(0)
SVG_WARN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l9 16H3z"/><path d="M12 10v4.5M12 17v.5"/></svg>'
SVG_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3.5" width="14" height="17" rx="2.5"/><path d="M8.5 8.5h7M8.5 12h7M8.5 15.5h4.5"/></svg>'

def card(page, L, sec):
    title = T[page][L]
    href = 'ops/%s.html#lang=%s' % (page, L)
    if page == 'after-surgery': href = 'ops/after-surgery.html#lang=%s' % L
    p = poster(page, L)
    if p:
        th = '<span class="th"><img loading="lazy" decoding="async" src="%s" width="720" height="1280" alt=""></span>' % p
        chip = '<span class="chip v">%s</span>' % UI['vid'][L]
        cls = 'pc vd'
    elif os.path.exists('media/img/p/%s.webp' % page):
        th = '<span class="th"><img class="ph" loading="lazy" decoding="async" src="media/img/p/%s.webp" width="1200" height="800" alt=""></span>' % page
        chip = '<span class="chip">%s</span>' % UI['txt'][L]
        cls = 'pc'
    else:
        th = '<span class="th tx">%s</span>' % SVG_DOC
        chip = '<span class="chip">%s</span>' % UI['txt'][L]
        cls = 'pc'
    return '<a class="%s" href="%s">%s<span class="pt">%s</span>%s</a>' % (cls, href, th, title, chip)


BM = {'q': {'ru': 'Где болит? Нажмите на сустав', 'he': 'איפה כואב? לחצו על המפרק', 'ar': 'أين الألم؟ اضغطوا على المفصل', 'en': 'Where does it hurt? Tap a joint'},
 'pts': [('arm',136,86,'r',{'ru':'Плечо','he':'כתף','ar':'الكتف','en':'Shoulder'}),
         ('arm',45,208,'l',{'ru':'Запястье','he':'שורש היד','ar':'الرسغ','en':'Wrist'}),
         ('spine',100,128,'r',{'ru':'Позвоночник','he':'עמוד השדרה','ar':'العمود الفقري','en':'Spine'}),
         ('hip',115,190,'r',{'ru':'Бедро','he':'ירך','ar':'الورك','en':'Hip'}),
         ('knee',81,268,'l',{'ru':'Колено','he':'ברך','ar':'الركبة','en':'Knee'}),
         ('leg',121,334,'r',{'ru':'Лодыжка','he':'קרסול','ar':'الكاحل','en':'Ankle'})]}
def bodymap(L):
    g=['<div class="bmap"><h2 class="bmq">%s</h2><svg viewBox="-85 0 370 360" direction="ltr" role="img" aria-label="%s">' % (BM['q'][L],BM['q'][L]),
       '<defs><linearGradient id="bg_%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3dc"/><stop offset="1" stop-color="#8fcac0"/></linearGradient></defs>' % L,
       '<g class="fig" fill="none" stroke="url(#bg_%s)" stroke-linecap="round" stroke-linejoin="round">' % L,
       '<circle cx="100" cy="36" r="21" fill="url(#bg_%s)" stroke="none"/>' % L,
       '<path d="M100 58v14" stroke-width="14"/>',
       '<path d="M74 76Q100 68 126 76Q140 80 140 94L132 140Q128 160 128 186Q100 198 72 186Q72 160 68 140L60 94Q60 80 74 76Z" fill="url(#bg_%s)" stroke="none"/>' % L,
       '<path d="M68 88L54 150L46 206M132 88L146 150L154 206" stroke-width="14"/><circle cx="45" cy="216" r="8" fill="#a9d6ce" stroke="none"/><circle cx="155" cy="216" r="8" fill="#a9d6ce" stroke="none"/>',
       '<path d="M86 180L82 268L80 334M114 180L118 268L120 334" stroke-width="19"/><path d="M80 344h-12M120 344h12" stroke-width="10" stroke="#8fcac0"/>',
       '<path class="spl" d="M100 84V182" stroke="#fff" stroke-width="3" stroke-dasharray="2 7"/></g>']
    for i,(k,x,y,side,lab) in enumerate(BM['pts']):
        tx = x+22 if side=='r' else x-22
        anc = 'start' if side=='r' else 'end'
        g.append('<a href="#r_%s_%s" class="hs" style="--d:%ss"><circle class="rg" cx="%d" cy="%d" r="9"/><circle class="dt" cx="%d" cy="%d" r="7"/><text x="%d" y="%d" text-anchor="%s">%s</text></a>' % (k,L,i*0.45,x,y,x,y,tx,y+5,anc,lab[L]))
    g.append('</svg></div>')
    return ''.join(g)

out = {}
for L in LANGS:
    h = ['<div data-l="%s">' % L, '<p class="hi2">%s</p>' % UI['hi'][L],
         bodymap(L), '<div class="cards" id="top_%s"><h2 class="cardsh">%s</h2><p class="hint">%s</p><div class="cg">' % (L, UI['choose'][L], UI['hint'][L])]
    for key, img, pages, sub, name in SEC:
        h.append('<a class="card" href="#r_%s_%s"><img loading="lazy" decoding="async" src="media/img/%s.webp" width="900" height="600" alt=""><span>%s</span></a>' % (key, L, img, name[L]))
    h.append('</div><p class="ill">%s</p></div>' % UI['ill'][L])
    h.append('<a class="warnbar" href="ops/postop.html#lang=%s"><span class="wi">%s</span><span><b>%s</b><small>%s</small></span></a>' % (L, SVG_WARN, UI['warn_b'][L], UI['warn_s'][L]))
    for key, img, pages, sub, name in SEC:
        h.append('<section class="reg" id="r_%s_%s"><h2 class="regh"><img src="media/img/%s.webp" width="900" height="600" alt="">%s</h2><div class="pg">' % (key, L, img, name[L]))
        h += [card(p, L, key) for p in pages]
        h.append('</div>')
        if sub:
            h.append('<h3 class="subh">%s</h3><div class="pg">' % sub[1][L])
            h += [card(p, L, key) for p in sub[0]]
            h.append('</div>')
        h.append('<a class="totop" href="#top_%s">↑ %s</a></section>' % (L, UI['top'][L]))
    h.append(grab(L, r'<div class="note">.*?</div>'))
    h.append(grab(L, r'<div class="disc">.*?</div>'))
    h.append('<a class="maplink" href="ops/sitemap.html#lang=%s"><span>%s</span></a>' % (L, UI['map'][L]))
    h.append('</div>')
    out[L] = ''.join(h)

a = s.find('<main>') + len('<main>')
b = s.find('</main>')
s2 = s[:a] + ''.join(out[L] for L in LANGS) + s[b:]
open('index.html', 'w', encoding='utf8').write(s2)
# coverage check
missing = [p for p in T if p not in s2.split('ops/sitemap')[0] and 'ops/%s.html' % p not in s2]
print('missing pages:', missing)
