#!/usr/bin/env python3
"""Готовность сайта к запуску для пациентов.

python3 tools/launch.py           — только проверка (ничего не меняет)
python3 tools/launch.py --apply   — снять плашку «Предварительная версия» (div.pv) со всех страниц

Проверка: плашки, заглушки «Видео в разработке» по языкам, битые локальные
ссылки/файлы (href/src/poster), запрещённые слова. Код выхода 1, если есть
битые ссылки или запрещённые слова (тогда --apply не выполняется).
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PV = re.compile(r'<div class="pv">.*?</div>', re.S)
LANGBLK = re.compile(r'<div data-l="(ru|he|ar|en|am)">')
BANNED = ['Кармель', 'כרמל', 'Carmel', 'الكرمل']
ATTR = re.compile(r'(?:href|src|poster)="([^"#?]+)(?:[?#][^"]*)?"')

pages = sorted(p for p in glob.glob('**/*.html', recursive=True) if not p.startswith('.git'))
broken, banned, banners, soon = [], [], [], {}
for p in pages:
    s = open(p, encoding='utf-8').read()
    if PV.search(s):
        banners.append(p)
    for w in BANNED:
        if w in s:
            banned.append(f'{p}: «{w}»')
    base = os.path.dirname(p)
    for u in set(ATTR.findall(s)):
        if re.match(r'^(https?:|mailto:|tel:|data:|javascript:|//)', u) or not u.strip():
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, u))):
            broken.append(f'{p} → {u}')
    if 'class="vsoon"' in s and not p.endswith('sitemap.html'):
        langs = []
        marks = [(m.start(), m.group(1)) for m in LANGBLK.finditer(s)]
        for m in re.finditer(r'class="vsoon"', s):
            prev = [l for pos, l in marks if pos < m.start()]
            langs.append(prev[-1] if prev else '?')
        soon[p] = langs

print(f'Страниц: {len(pages)}; с плашкой: {len(banners)}')
print(f'Заглушки «Видео в разработке» ({sum(map(len, soon.values()))}):')
for p, l in soon.items():
    print(f'  {p}: {",".join(l)}')
print(f'Битые ссылки: {len(broken)}')
for b in broken[:40]:
    print('  ' + b)
print(f'Запрещённые слова: {len(banned)}')
for b in banned:
    print('  ' + b)

bad = bool(broken or banned)
if '--apply' in sys.argv:
    if bad:
        print('НЕ ПРИМЕНЕНО: сначала исправить битые ссылки / запрещённые слова')
        sys.exit(1)
    for p in banners:
        s = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(PV.sub('', s))
    print(f'Плашка снята на {len(banners)} страницах')
sys.exit(1 if bad else 0)
