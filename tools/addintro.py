#!/usr/bin/env python3
"""Шаг «Введение» (step0_<l>) в начало маршрутов ops/*-path.html; идемпотентно."""
import re,glob,sys
idx=open('index.html').read()
SVG=re.search(r'<a class="warnbar" href="ops/postop.html#lang=ru"><span class="wi">(<svg.*?</svg>)',idx,re.S).group(1)
T={
'ru':('Введение',['Здесь — весь путь по шагам: подготовка, операция, первые дни в отделении, выписка и реабилитация (шикум). В каждом шаге есть короткие видео: нажмите на карточку, чтобы открыть тему.','Язык можно сменить кнопками вверху страницы. Меню ☰ и поиск есть на каждой странице.']),
'he':('מבוא',['כאן תמצאו את כל הדרך לפי הסדר: הכנה, הניתוח, הימים הראשונים במחלקה, שחרור ושיקום. בכל שלב יש סרטונים קצרים: לחצו על כרטיס כדי לפתוח את הנושא.','אפשר להחליף שפה בכפתורים בראש העמוד. בכל עמוד יש תפריט ☰ וחיפוש.']),
'ar':('مقدمة',['هنا تجدون الطريق كله خطوة بخطوة: التحضير، العملية، الأيام الأولى في القسم، الخروج من المستشفى، وإعادة التأهيل. في كل خطوة مقاطع فيديو قصيرة: اضغطوا على البطاقة لفتح الموضوع.','يمكنكم تغيير اللغة بالأزرار في أعلى الصفحة. في كل صفحة قائمة ☰ وبحث.']),
'en':('Introduction',['Here is the whole journey, step by step: preparation, your operation, the first days on the ward, discharge and rehabilitation. Each step has short videos: tap a card to open the topic.','Change the language with the buttons at the top of the page. Every page has the ☰ menu and search.']),
}
thr=open('ops/thr.html').read()
DISC=dict(zip(['ru','he','ar','en'],re.findall(r'<div class="disc">[^<]*</div>',thr)[:4]))
for l in T:
    m=re.search(r'<a class="warnbar" href="ops/postop.html#lang=%s"><span class="wi"><svg.*?</svg></span>(.*?)</a>'%l,idx,re.S)
    T[l]+=(m.group(1),)
n=0
for f in sorted(glob.glob('ops/*-path.html')):
    s=open(f).read()
    for l,(h,ps,wb) in T.items():
        if f'id="step0_{l}"' in s: continue
        li=(f'<li class="pstep pintro" id="step0_{l}"><span class="pnum" aria-hidden="true">i</span><div class="pbody"><h2>{h}</h2>'
            +''.join(f'<p>{p}</p>' for p in ps)
            +f'<a class="warnbar" href="postop.html#lang={l}"><span class="wi">{SVG}</span>{wb}</a>{DISC[l]}</div></li>')
        k=f'<li class="pstep" id="step1_{l}">'
        assert s.count(k)==1,(f,l)
        s=s.replace(k,li+k); n+=1
    open(f,'w').write(s)
print('вставлено',n)
