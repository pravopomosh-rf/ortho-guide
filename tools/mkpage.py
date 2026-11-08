#!/usr/bin/env python3
"""mkpage.py SPEC.json TEMPLATE.html OUT.html
Собирает страницу темы из JSON (title, secs[h, li], src[]) на 4 языках,
беря шапку, плашку, блок «Защита от инфекции» и подвал из готовой страницы-шаблона."""
import json, re, sys, html as H
spec, tpl, out = sys.argv[1:4]
d = json.load(open(spec)); s = open(tpl).read()
L = ['ru', 'he', 'ar', 'en']
e = lambda x: H.escape(x, quote=False)
# шапка: заменить h1 в каждом языке
head_end = s.index('<main>')
head = s[:head_end]
for l in L:
    head = re.sub(r'(<div data-l="%s"><a class="back"[^>]*>[^<]*</a><div class="d">[^<]*</div><h1>)[^<]*(</h1>)' % l,
                  lambda m: m.group(1) + e(d['title'][l]) + m.group(2), head)
VIDEO = {'ru': 'Видео', 'he': 'סרטון', 'ar': 'فيديو', 'en': 'Video'}
SOON = {'ru': 'Видео в разработке — скоро появится здесь.', 'he': 'הסרטון בהכנה — יופיע כאן בקרוב.',
        'ar': 'الفيديو قيد الإعداد — سيظهر هنا قريبًا.', 'en': 'Video in preparation — coming here soon.'}
SRC = {'ru': 'Официальные источники', 'he': 'מקורות רשמיים', 'ar': 'مصادر رسمية', 'en': 'Official sources'}
body = '<main>'
for l in L:
    # видео-слот берём из шаблона, если есть, иначе стандартный
    m = re.search(r'<section id="video_%s".*?</section>' % l, s, re.S)
    vid = m.group(0) if m and d.get('keep_video') else (
        f'<section id="video_{l}" class="vtop vdev"><div class="vlabel"><span class="vplay" aria-hidden="true"></span>'
        f'<span>{VIDEO[l]}</span></div><p class="vsoon">{SOON[l]}</p></section>')
    parts = [f'<div data-l="{l}">', vid]
    for i, sec in enumerate(d['secs']):
        lis = ''.join(f'<li>{li[l] if li.get("html") else e(li[l])}</li>' for li in sec['li'])
        parts.append(f'<section id="s{i}_{l}"><h2>{e(sec["h"][l])}</h2><ul>{lis}</ul></section>')
    for blk in d.get('blocks', []):
        m = re.search(r'<section id="%s_%s".*?</section>' % (blk, l), s, re.S)
        if m: parts.append(m.group(0))
    srcs = ''.join((f'<li><a href="{x["url"]}" target="_blank" rel="noopener">{e(x["t"])}</a></li>' if x.get("url") else f'<li>{e(x["t"])}</li>') for x in d['src'])
    parts.append(f'<section id="s{len(d["secs"])}_{l}"><h2>{SRC[l]}</h2><ol>{srcs}</ol></section>')
    m = re.search(r'<div data-l="%s">.*?(<div class="disc">.*?</div>)</div>' % l, s[head_end:], re.S)
    disc = re.findall(r'<div class="disc">.*?</div>', s[head_end:])[L.index(l)]
    parts.append(disc + '</div>')
    body += ''.join(parts)
body += '</main><script src="../app.js"></script></body></html>'
open(out, 'w').write(head + body)
print('ok', out, len(head + body))
