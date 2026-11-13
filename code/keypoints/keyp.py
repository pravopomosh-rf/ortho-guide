"""Insert/replace 'Главное за 30 секунд' block before the video section in ops/PAGE.html.
usage: keyp.py SITE_DIR data.txt  (data in ChatGPT format: ### page / RU1: ...)"""
import sys,re,html
site,data=sys.argv[1],sys.argv[2]
H={'ru':'Главное за 30 секунд','he':'העיקר בחצי דקה','ar':'الأهم في نصف دقيقة','en':'Key points in 30 seconds'}
pages={};cur=None
for l in open(data,encoding='utf-8'):
    l=l.strip()
    m=re.match(r'###\s*([\w-]+)',l)
    if m: cur=pages.setdefault(m.group(1),{}); continue
    m=re.match(r'(RU|HE|AR|EN)([123])\s*:\s*(.+)',l)
    if m and cur is not None: cur.setdefault(m.group(1).lower(),{})[int(m.group(2))]=m.group(3).strip()
for p,d in pages.items():
    f=f'{site}/ops/{p}.html'; s=open(f,encoding='utf-8').read()
    for L in ['ru','he','ar','en']:
        items=[d[L][k] for k in (1,2,3)]
        blk=f'<section class="key" id="key_{L}"><h2>{H[L]}</h2><ul>'+''.join(f'<li>{html.escape(x,quote=False)}</li>' for x in items)+'</ul></section>'
        s=re.sub(rf'<section class="key" id="key_{L}">.*?</section>','',s,flags=re.S)
        m=s.find('<main>'); i=s.find(f'<div data-l="{L}">',m)
        assert i>0,(p,L)
        j=i+len(f'<div data-l="{L}">')
        s=s[:j]+blk+s[j:]
    open(f,'w',encoding='utf-8').write(s); print('ok',p)
