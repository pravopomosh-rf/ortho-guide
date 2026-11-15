#!/usr/bin/env python3
"""restage.py PAGE MAPJSON DOSJSON — перестраивает страницу операции по этапам 1..5.
map: {"I":[ids], "1":[...], ..., "5":[...]}; ids без _lang; "video:N" — N-я часть (по <h3>) секции video."""
import re, json, sys, html as H
L = ['ru', 'he', 'ar', 'en']
page, mp, dos = sys.argv[1], json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))
s = open(page).read()
if 'class="stnav"' in s: print('already', page); sys.exit(0)
e = lambda x: H.escape(x, quote=False)
ADMT = {'ru': 'Поступление в отделение: что вас ожидает', 'he': 'קבלה למחלקה: מה צפוי לכם', 'ar': 'الدخول إلى القسم: ماذا ينتظركم', 'en': 'Admission to the ward: what to expect'}
CHIP = {'ru': 'Памятка', 'he': 'דף מידע', 'ar': 'صفحة معلومات', 'en': 'Leaflet'}
PREV = {'ru': ('preopv_ru', 9), 'he': ('preopv_he', 9), 'ar': ('preop_ar', 16)}
PRET = {'ru': 'Видео: подготовка к операции', 'he': 'סרטון: הכנה לניתוח', 'ar': 'فيديو: التحضير للعملية', 'en': 'Preparing for surgery'}
PREL = {'ru': 'Подробно — на странице «Подготовка к операции».', 'he': 'מידע מפורט בעמוד ״הכנה לניתוח״.', 'ar': 'للتفاصيل راجعوا صفحة «التحضير للعملية».', 'en': 'Full details: the “Preparing for surgery” page.'}
NAVL = {'ru': 'Этапы', 'he': 'שלבים', 'ar': 'المراحل', 'en': 'Steps'}
ADMLINK = {'ru': '«Поступление в отделение»', 'he': '״קבלה למחלקה״', 'ar': '«الدخول إلى القسم»', 'en': '“Admission to the ward”'}

def lis(items, l, link=None):
    out = ''
    for li in items:
        t = e(li[l])
        out += f'<li>{t}</li>'
    return out

def adm_block(l):
    items = dos['adm']['li']
    body = ''.join(f'<li>{e(x[l])}</li>' for x in items[:-1])
    card = (f'<div class="pg stcard"><a class="pc" href="admission.html#lang={l}"><span class="th"><img class="ph" loading="lazy" decoding="async" '
            f'src="../media/img/p/admission.webp" width="1200" height="800" alt=""></span><span class="pt">{ADMT[l]}</span><span class="chip">{CHIP[l]}</span></a></div>')
    return f'<section id="adm_{l}"><h2>{e(dos["adm"]["h"][l])}</h2><ul>{body}</ul>{card}</section>'

def prep_block(l):
    if l in PREV:
        n, a = PREV[l]
        wh = 'width="1080" height="1920" style="aspect-ratio:1080/1920"' if a == 9 else 'width="1280" height="720" style="aspect-ratio:1280/720"'
        v = f'<video class="vid v{a}" {wh} controls preload="none" playsinline poster="../video/{n}.jpg" src="../video/{n}.mp4"></video>'
        return (f'<section id="prepv_{l}" class="vtop"><div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{PRET[l]}</span></div>'
                f'{v}<p style="margin-top:10px"><a href="preop.html#lang={l}">{PREL[l]}</a></p></section>')
    return (f'<section id="prepv_{l}"><h2>{PRET[l]}</h2><p><a href="preop.html#lang={l}">{PREL[l]}</a></p></section>')

def day_block(l):
    return f'<section id="day_{l}"><h2>{e(dos["day"]["h"][l])}</h2><ul>{"".join(f"<li>{e(x[l])}</li>" for x in dos["day"]["li"])}</ul></section>'

def split_video(sec, l):
    """делит секцию video на части по <h3>; возвращает список секций"""
    m = re.match(r'(<section id="video_%s"[^>]*>)(.*)</section>$' % l, sec, re.S)
    head, inner = m.group(1), m.group(2)
    lab = re.match(r'(<div class="vlabel">.*?</div>)(<h2>.*?</h2>)?', inner, re.S)
    pre = lab.group(1) if lab else ''
    rest = inner[lab.end():] if lab else inner
    parts = re.split(r'(?=<h3)', rest)
    parts = [p for p in parts if p.startswith('<h3')]
    out = []
    for k, p in enumerate(parts):
        p = re.sub(r'<p style="margin-top:10px">.*?</p>$', '', p, flags=re.S)
        out.append(f'<section id="video{k}_{l}" class="vtop">{pre}{p}</section>')
    return out

i0 = s.index('<main>')
newmain = s[:i0] + '<main>'
body = s[i0 + 6:]
for l in L:
    a = body.index(f'<div data-l="{l}">')
    # конец блока языка = начало следующего <div data-l= или </main>
    nxt = [body.find(f'<div data-l="{x}">', a + 5) for x in L if x != l]
    nxt = [x for x in nxt if x > a] + [body.index('</main>')]
    b = min(nxt)
    blk = body[a + len(f'<div data-l="{l}">'):b]
    secs = re.findall(r'<section[^>]*>.*?</section>', blk, re.S)
    tail = blk[blk.rfind('</section>') + 10:]
    byid = {}
    for sc in secs:
        sid = re.match(r'<section[^>]*id="([^"]+)_%s"' % l, sc)
        assert sid, sc[:80]
        byid[sid.group(1)] = sc
    if any(x.startswith('video:') for st in mp.values() for x in st):
        for k, p in enumerate(split_video(byid['video'], l)):
            byid[f'video:{k}'] = p
    used = set()
    def take(ids):
        out = ''
        for x in ids:
            if x in byid: out += byid[x]; used.add(x)
            else: print('WARN missing', page, l, x)
        return out
    nav = ''.join(f'<a href="#st{k}_{l}"><b>{k}</b>{e(dos["stages"]["s"+str(k)][l])}</a>' for k in range(1, 6))
    out = f'<div data-l="{l}">' + take(mp.get('key', ['key']))
    out += f'<nav class="stnav" aria-label="{NAVL[l]}">{nav}</nav>'
    out += take(mp['I'])
    extra = {1: adm_block(l), 2: prep_block(l), 3: day_block(l)}
    for k in range(1, 6):
        st = f'<div class="stage" id="st{k}_{l}"><div class="sthead"><span class="pnum" aria-hidden="true">{k}</span><h2>{e(dos["stages"]["s"+str(k)][l])}</h2></div>'
        inner = ''
        if k == 1: inner += take(mp.get('1', [])) + extra[1]
        elif k == 2: inner += extra[2] + take(mp.get('2', []))
        elif k == 3: inner += take(mp.get('3', [])) + extra[3]
        else: inner += take(mp.get(str(k), []))
        out += st + inner + '</div>'
    rest = [x for x in byid if x not in used and not x.startswith('video:') and not (x == 'video' and 'video:0' in byid)]
    srcid = [x for x in rest if x.startswith('src') or x == rest[-1]]
    leftover = [x for x in rest if x not in srcid]
    if leftover: print('WARN leftover', page, l, leftover)
    out += take(leftover) + take(srcid) + tail
    newmain += out
    body = body[:a] + '\0' * (b - a) + body[b:]  # mark consumed
end = body.index('</main>')
newmain += body[end:]
newmain = newmain.replace('style.css?v=1411b', 'style.css?v=1511s')
open(page, 'w').write(newmain)
print('ok', page)
