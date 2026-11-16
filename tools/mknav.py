#!/usr/bin/env python3
# mknav.py — строит nav-data.js для меню и поиска (nav.js) из index.html и ops/*.html.
# Запуск из корня репо: python3 tools/mknav.py   (перезапускать после добавления/изменения страниц)
import re, glob, html, json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LS = ['ru', 'he', 'ar', 'en']
T = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
idx = open(R + '/index.html', encoding='utf8').read()

def block(s, L):
    """HTML языкового блока data-l=L внутри main/header страницы (все блоки этого языка подряд)."""
    out = []
    for m in re.finditer(r'<div data-l="%s">' % L, s):
        i = m.end(); depth = 1; j = i
        for t in re.finditer(r'<(/?)div\b[^>]*>', s[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: j = i + t.start(); break
        out.append(s[i:j])
    return ' '.join(out)

EXTRA = {'wrist-path.html': 'arm'}
def block_h(s, L):
    i = s.find('<header>'); j = s.find('</header>')
    return block(s[i:j], L)

D = {}
pages = {}
for f in sorted(glob.glob(R + '/ops/*.html')):
    name = os.path.basename(f)
    if name == 'sitemap.html': continue
    s = open(f, encoding='utf8').read()
    pages[name] = s

for L in LS:
    secs, docs, seen = [], [], {}
    for m in re.finditer(r'<section class="reg" id="r_(\w+)_%s"><h2 class="regh">(?:<img[^>]*src="([^"]*)"[^>]*>)?(.*?)</h2>(.*?)</section>' % L, idx, re.S):
        key, img, title, body = m.group(1), m.group(2), T(m.group(3)), m.group(4)
        items = []
        pb = re.search(r'<a class="pathbar" href="([^"#]*)#lang=%s"[^>]*>.*?<b>(.*?)</b>' % L, body, re.S)
        if pb: items.append({'t': T(pb.group(2)), 'h': pb.group(1), 'p': 1})
        for c in re.finditer(r'<a class="pc( vd)?" href="([^"#]*)#lang=%s">.*?<span class="pt">(.*?)</span>' % L, body, re.S):
            items.append({'t': T(c.group(3)), 'h': c.group(2), 'v': 1 if c.group(1) else 0})
        # маршруты, которых нет на главной (например, запястье) — в свой раздел
        for pn, sk in EXTRA.items():
            if sk == key and pn in pages and not any(x['h'] == 'ops/' + pn for x in items):
                h1 = re.search(r'<h1>(.*?)</h1>', block_h(pages[pn], L), re.S)
                if h1: items.insert(1 if pb else 0, {'t': T(h1.group(1)), 'h': 'ops/' + pn, 'p': 1})
        secs.append({'k': key, 't': title, 'i': img or '', 'items': items})
        for it in items:
            seen.setdefault(it['h'], (title, it))
    for h, (st, it) in seen.items():
        name = h.split('/')[-1]; s = pages.get(name)
        heads = []
        if s:
            b = block(s, L)
            heads = [T(x) for x in re.findall(r'<h[23][^>]*>(.*?)</h[23]>', b, re.S)]
            heads = [x for x in heads if 2 < len(x) < 120]
        bw = []
        if s:
            txt = re.sub(r'[^\w]+', ' ', re.sub(r'[\u0591-\u05C7\u064B-\u065F\u0670\u0640]', '', T(block(s, L)).lower().replace('ё', 'е')))
            bw = sorted(set(w for w in txt.split() if len(w) >= 6 and not w.isdigit()))
        docs.append({'t': it['t'], 'h': h, 's': st, 'v': it.get('v', 0), 'p': it.get('p', 0), 'k': ' | '.join(dict.fromkeys(heads)), 'b': bw})
    # слова текста страниц: только «отличительные» (встречаются не более чем на 8 страницах)
    import collections
    df = collections.Counter(w for d in docs for w in set(d['b']))
    for d in docs: d['b'] = ' '.join(w for w in d['b'] if df[w] <= 8)
    out = R + '/nav-%s.js' % L
    open(out, 'w', encoding='utf8').write('(window.NAVD=window.NAVD||{}).%s=' % L + json.dumps({'secs': secs, 'docs': docs}, ensure_ascii=False, separators=(',', ':')) + ';')
    print(L, len(secs), 'разделов,', len(docs), 'тем,', os.path.getsize(out), 'байт')
