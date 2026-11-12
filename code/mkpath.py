#!/usr/bin/env python3
# Генерирует ops/<slug>.html — страницу-маршрут «всё по порядку» из карточек главной (одобренные заголовки ×4)
# и вставляет кнопку-ссылку в начало раздела на главной. Запуск: mkpath.py REPO spine
import re, sys, json
repo, key = sys.argv[1], sys.argv[2]
cfg = json.load(open(__file__.replace('mkpath.py', 'paths.json'), encoding='utf8'))[key]
H = open(f'{repo}/index.html', encoding='utf8').read()
LANGS = ['ru', 'he', 'ar', 'en']

def card(L, page):
    m = re.search(r'<a class="pc[^"]*" href="ops/%s\.html#lang=%s">.*?</a>' % (re.escape(page), L), H, re.S)
    if not m: raise SystemExit(f'нет карточки {page} {L}')
    c = m.group(0)
    c = c.replace('href="ops/', 'href="').replace('src="media/', 'src="../media/').replace('src="video/', 'src="../video/')
    return c

def head_block(L, t):
    back = {'ru': '← Все темы', 'he': '→ כל הנושאים', 'ar': '→ كل المواضيع', 'en': '← All topics'}[L]
    dep = {'ru': 'Отделение ортопедии', 'he': 'מחלקה אורתופדית', 'ar': 'قسم جراحة العظام', 'en': 'Orthopedics Department'}[L]
    return f'<div data-l="{L}"><a class="back" href="../index.html#lang={L}">{back}</a><div class="d">{dep}</div><h1>{t["title"]}</h1></div>'

DISC = {'ru': 'Это общая информация. Индивидуальные указания лечащего врача имеют приоритет над рекомендациями на этой странице.',
        'he': 'זהו מידע כללי. להנחיות האישיות של הרופא המטפל יש עדיפות על ההמלצות בדף זה.',
        'ar': 'هذه معلومات عامة. تعليمات الطبيب المعالج الخاصة بحالتكم لها الأولوية على التوصيات الواردة في هذه الصفحة.',
        'en': "This is general information. Your treating doctor's individual instructions take priority over the recommendations on this page."}

out = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">',
       f'<title>{cfg["he"]["title"]}</title><link rel="stylesheet" href="../style.css"></head><body><header>']
out += [head_block(L, cfg[L]) for L in LANGS]
out.append('<div class="lang" role="group" aria-label="Language / שפה / اللغة / Язык"><button type="button" data-k="ru" aria-pressed="false" onclick="setL(\'ru\')">Русский</button><button type="button" data-k="he" aria-pressed="false" onclick="setL(\'he\')">עברית</button><button type="button" data-k="ar" aria-pressed="false" onclick="setL(\'ar\')">العربية</button><button type="button" data-k="en" aria-pressed="false" onclick="setL(\'en\')">English</button></div></header>')
out.append('<div class="pv"><span data-l="ru">Предварительная версия — не для пациентов</span><span data-l="he">גרסה מקדימה — לא למטופלים</span><span data-l="ar">نسخة تجريبية — ليست للمرضى</span><span data-l="en">Preview version — not for patients</span></div><main>')
for L in LANGS:
    t = cfg[L]
    out.append(f'<div data-l="{L}"><p class="pathlead">{t["lead"]}</p><ol class="path">')
    for i, st in enumerate(cfg['steps']):
        s = t['steps'][i]
        hint = f'<p class="hint">{s["hint"]}</p>' if s.get('hint') else ''
        cards = ''.join(card(L, p) for p in st)
        out.append(f'<li class="pstep" id="step{i+1}_{L}"><span class="pnum" aria-hidden="true">{i+1}</span><div class="pbody"><h2>{s["h"]}</h2>{hint}<div class="pg">{cards}</div></div></li>')
    out.append(f'</ol><div class="disc">{DISC[L]}</div></div>')
out.append('</main><script src="../app.js"></script></body></html>')
open(f'{repo}/ops/{cfg["slug"]}.html', 'w', encoding='utf8').write(''.join(out))

# кнопка на главной — в начале раздела
for L in LANGS:
    t = cfg[L]
    btn = (f'<a class="pathbar" href="ops/{cfg["slug"]}.html#lang={L}"><span class="pwi" aria-hidden="true">1·2·3·4</span>'
           f'<span><b>{t["btn"]}</b><small>{t["btn_sub"]}</small></span></a>')
    sec = f'<section class="reg" id="r_{cfg["section"]}_{L}">'
    i = H.find(sec); assert i >= 0, sec
    j = H.find('</h2>', i) + 5
    k = H.find('</section>', i)
    if f'ops/{cfg["slug"]}.html#lang={L}' in H[i:k]:
        H = H[:j] + re.sub(r'<a class="pathbar".*?</a>', btn, H[j:k], count=1, flags=re.S) + H[k:]
    else:
        H = H[:j] + btn + H[j:]
open(f'{repo}/index.html', 'w', encoding='utf8').write(H)

css = open(f'{repo}/style.css', encoding='utf8').read()
if '.pathbar' not in css:
    css += ('\n.pathbar{display:flex;align-items:center;gap:14px;margin:0 0 14px;padding:14px 16px;border-radius:18px;background:var(--teal-l);border:1px solid #bfe0d8;color:inherit;text-decoration:none;box-shadow:var(--shadow)}'
            '\n.pathbar .pwi{flex:none;min-width:46px;height:46px;padding:0 8px;border-radius:14px;display:grid;place-items:center;background:var(--teal);color:#fff;font-weight:700;font-size:13px;direction:ltr}'
            '\n.pathbar b{display:block;font-size:18px;color:var(--teal-d)}'
            '\n.pathbar small{display:block;font-size:15px;color:var(--ink2);margin-top:2px}'
            '\n.pathlead{font-size:18px;margin:16px 0 8px;color:var(--ink2)}'
            '\nol.path{list-style:none;margin:0;padding:0}'
            '\n.pstep{position:relative;display:flex;gap:12px;padding:0 0 18px}'
            '\n.pstep:not(:last-child)::before{content:"";position:absolute;inset-inline-start:19px;top:44px;bottom:0;width:2px;background:var(--line)}'
            '\n.pnum{flex:none;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--teal);color:#fff;font-weight:700;font-size:18px;box-shadow:var(--shadow);position:relative;z-index:1}'
            '\n.pbody{flex:1;min-width:0}'
            '\n.pbody h2{margin:6px 0 6px;font-size:21px}'
            '\n.pbody .hint{margin:0 0 10px;color:var(--ink2)}\n')
    open(f'{repo}/style.css', 'w', encoding='utf8').write(css)
print('ok', cfg['slug'])
