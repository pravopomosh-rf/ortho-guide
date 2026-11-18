import json,re,sys
d=json.load(open('/mnt/user-data/uploads/Downloads/research_gpt_1811.json'))
R='/home/claude/ortho-guide/'
s=open(R+'ops/sitemap.html').read()
head=s[:s.find('<header>')]
head=re.sub(r'<style>.*?</style>','<style>.rcard{border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0;background:#fff}.rcard p{margin:0;line-height:1.55}.rsrc{font-size:14px;margin-top:8px;color:#555}.rsrc a{color:var(--teal)}.rdisc{background:#fff7e6;border:1px solid #f0d28a;border-radius:12px;padding:12px 14px;margin:14px 0;font-size:16px}.rdate{color:#6b7280;font-size:14px}</style>',head,flags=re.S)
hdr=s[s.find('<header>'):s.find('</header>')+9]
T={'ru':('Исследования: что нового в мире','Обзор научных публикаций для специалистов и интересующихся пациентов. Раздел регулярно обновляется.'),
'he':('מחקרים: מה חדש בעולם','סקירת פרסומים מדעיים לאנשי מקצוע ולמטופלים המתעניינים. הדף מתעדכן באופן קבוע.'),
'ar':('أبحاث: ما الجديد في العالم','مراجعة للمنشورات العلمية للمختصين وللمرضى المهتمين. يُحدَّث هذا القسم بانتظام.'),
'en':('Research: what is new worldwide','A review of scientific publications for professionals and interested patients. This section is updated regularly.')}
hdr=re.sub(r'(<div data-l="(ru|he|ar|en)">.*?<h1>)[^<]*(</h1>)',lambda m:m.group(1)+T[m.group(2)][0]+m.group(3),hdr,flags=re.S)
hdr=re.sub(r'<div data-l="am">.*?</h1></div>','',hdr,flags=re.S)
head=re.sub(r'<title>[^<]*</title>','<title>'+T['he'][0]+'</title>',head)
pv=s[s.find('<div class="pv">'):s.find('<main>')]
PM=lambda t: re.sub(r'PMID (\d+)',r'<a href="https://pubmed.ncbi.nlm.nih.gov/\1/" target="_blank" rel="noopener">PMID \1</a>',t)
SRC=d.get('sources') or d.get('r_sources')
def src(k):
    v=SRC.get(k)
    if not v: return ''
    out=[]
    for part in v.split(' ; '):
        m=re.search(r'(https?://\S+)$',part.strip())
        if m: out.append('<a href="'+m.group(1)+'" target="_blank" rel="noopener">'+esc(part[:m.start()].rstrip(': ').strip())+'</a>')
        else: out.append(esc(part))
    return '<p class="rsrc">'+'; '.join(out)+'</p>'
def esc(t): return t.replace('&','&amp;').replace('<','&lt;')
main='<main>'
for L in ['ru','he','ar','en']:
    g=lambda k: d.get(f'r_{k}_{L}','')
    b=f'<div data-l="{L}"><section id="s0_{L}"><p>{T[L][1]}</p><p class="rdisc">{esc(g("disc"))}</p></section>'
    for a,n in [('a1',10),('a2',3)]:
        b+=f'<section id="{a}_{L}"><h2>{esc(g(a+"_title"))}</h2><p>{PM(esc(g(a+"_intro")))}</p>'+src(a+'_intro')
        for i in range(1,n+1):
            t=g(f'{a}_c{i}')
            if t: b+=f'<div class="rcard"><p>{PM(esc(t))}</p>'+src(f'{a}_c{i}')+'</div>'
        b+=f'<p class="rdisc">{esc(g("disc"))}</p></section>'
    b+=f'<p class="rdate">{esc(g("a2_note"))}</p></div>'
    main+=b
main+='</main>'
tail='<script src="../app.js?v=1711a"></script><script src="../nav.js?v=1811r" defer></script></body></html>'
open(R+'ops/research.html','w').write(head+hdr+pv+main+tail)
print('ok', len(head+hdr+pv+main))
