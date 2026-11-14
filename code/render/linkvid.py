# linkvid.py PAGE BASE L1 [L2..] — карточки (главная, маршруты) → видео; карта сайта → vchip со списком языков
import sys,re,glob
page,base,langs=sys.argv[1],sys.argv[2],sys.argv[3:]
R='/home/claude/ortho-guide/'
CH={'ru':'▶ Видео','he':'▶ סרטון','ar':'▶ فيديو','en':'▶ Video'}
VC={'ru':('▶ Видео:',{'ru':'русский','he':'иврит','ar':'арабский','en':'английский'}),
    'he':('▶ סרטון:',{'ru':'רוסית','he':'עברית','ar':'ערבית','en':'אנגלית'}),
    'ar':('▶ فيديو:',{'ru':'الروسية','he':'العبرية','ar':'العربية','en':'الإنجليزية'}),
    'en':('▶ Video:',{'ru':'Russian','he':'Hebrew','ar':'Arabic','en':'English'})}
ORD=['ru','he','ar','en']
for f in [R+'index.html']+glob.glob(R+'ops/*-path.html'):
    s=open(f,encoding='utf8').read(); pre='' if f.endswith('index.html') else '../'; hp='ops/' if not pre else ''; n=0
    for L in langs:
        pat=re.compile(r'<a class="pc" href="'+hp+re.escape(page)+'#lang='+L+r'"><span class="th"><img class="ph" loading="lazy" decoding="async" src="[^"]*" width="\d+" height="\d+" alt=""></span><span class="pt">([^<]*)</span><span class="chip">[^<]*</span></a>')
        s,k=pat.subn(lambda m:f'<a class="pc vd" href="{hp}{page}#lang={L}"><span class="th"><img loading="lazy" decoding="async" src="{pre}video/{base}_{L}.jpg" width="720" height="1280" alt=""></span><span class="pt">{m.group(1)}</span><span class="chip v">{CH[L]}</span></a>',s); n+=k
    open(f,'w',encoding='utf8').write(s); print(f.split('/')[-1],n)
f=R+'ops/sitemap.html'; s=open(f,encoding='utf8').read(); n=0
for S in ORD:
    lab,nm=VC[S]; ch=' '.join(f'<a class="vlang" href="{page}#lang={L}">{nm[L]}</a>' for L in ORD if L in langs)
    pat=re.compile(r'(<li><a href="'+re.escape(page)+'#lang='+S+r'">[^<]*</a> )<span class="(?:mnone|vchip)">.*?</span></li>')
    s,k=pat.subn(lambda m:m.group(1)+f'<span class="vchip">{lab} {ch}</span></li>',s,count=1); n+=k
open(f,'w',encoding='utf8').write(s); print('sitemap',n)
