import re,glob,os,sys
os.chdir(sys.argv[1])
L=['ru','he','ar','en']
blk=re.compile(r'<div data-l="(ru|he|ar|en|am)">')
rows=[]
for p in sorted(glob.glob('ops/*.html'))+['index.html']:
    s=open(p,encoding='utf-8').read()
    t=re.search(r'<title>(.*?)</title>',s,re.S); t=(t.group(1).strip() if t else p)[:60]
    marks=[(m.start(),m.group(1)) for m in blk.finditer(s)]
    def lang_at(pos):
        prev=[l for q,l in marks if q<pos]; return prev[-1] if prev else '*'
    vids={l:set() for l in L+['am','*']}
    for m in re.finditer(r'<(?:video|source)[^>]*src="([^"?]+\.mp4)',s):
        vids[lang_at(m.start())].add(os.path.basename(m.group(1)))
    soon={lang_at(m.start()) for m in re.finditer(r'class="vsoon"',s)}
    have={l for _,l in marks}
    cells=[]
    for l in L:
        if l not in have and not vids['*']: cells.append('—')
        elif l in soon: cells.append('заглушка')
        else:
            n=len(vids[l]) or len({v for v in vids['*'] if f'_{l}.' in v})
            cells.append(f'стр✓ видео {n}' if n else 'стр✓ без видео')
    rows.append((p,t,cells))
print('| Страница | ru | he | ar | en |'); print('|---|---|---|---|---|')
for p,t,c in rows: print(f'| {p} — {t} | '+' | '.join(c)+' |')
