# vfirst.py — Георгий 16.11: страница раздела начинается с фото, затем ВСЕ видео, потом текст.
# Для каждой ops/*.html (кроме *-path, sitemap): в каждом языковом блоке <div data-l=..> в <main>
# 1) фото-шапка figure.tophero; 2) section.vfirst со всеми видео страницы (с подписями); 3) остальной текст.
import re,glob,os,sys,html
R='/home/claude/ortho-guide/'
HERO={'thr':'sec_hip.webp','thr-anterior':'sec_hip.webp','hip-fracture':'sec_hip.webp','tkr':'sec_knee.webp','knee-arthroscopy':'sec_knee.webp',
 'laminectomy':'sec_spine.webp','kyphoplasty':'sec_spine.webp','fusion-discectomy':'sec_spine.webp','rotator-cuff':'p/sec_arm.webp',
 'shoulder-replacement':'p/sec_arm.webp','ankle-fracture':'p/sec_leg.webp','amputation':'p/sec_leg.webp','preop':'sec_preop.webp',
 'after-anaesthesia':'sec_after.webp','oxygen-sleep':'sec_after.webp','enoxaparin-injections':'sec_home.webp','rehab':'sec_home.webp'}
T={'ru':'Сначала посмотрите видео','he':'קודם כל, צפו בסרטונים','ar':'أولًا، شاهدوا الفيديو','en':'Start with the videos','am':'Start with the videos'}
T1={'ru':'Сначала посмотрите видео','he':'קודם כל, צפו בסרטון','ar':'أولًا، شاهدوا الفيديو','en':'Start with the video','am':'Start with the video'}
def hero(slug):
    p=f'p/{slug}.webp'
    if os.path.exists(R+'media/img/'+p): return p
    return HERO.get(slug)
def txt(h): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',h))).strip()
def proc(block,L,slug):
    if 'class="tophero"' in block or 'class="vfirst"' in block: return block
    items=[]
    def take(m):
        return m.group(0)
    # найти все видео
    out=block; vids=list(re.finditer(r'<video\b[^>]*>.*?</video>',out,re.S))
    for v in reversed(vids):
        a,b=v.span(); vid=v.group(0)
        # секция, в которой лежит видео
        ss=out.rfind('<section',0,a); se=out.find('</section>',b)
        sec=out[ss:se+10] if ss>=0 and se>0 else ''
        label=''; link=''
        pre=out[ss:a] if ss>=0 else ''
        mv=re.search(r'<div class="vlabel">(.*?)</div>\s*$',pre,re.S)
        m3=re.search(r'<h3[^>]*>(.*?)</h3>\s*$',pre,re.S)
        m2=re.search(r'<h2[^>]*>(.*?)</h2>',sec,re.S)
        cut_a=a
        if mv: label=txt(mv.group(1)); cut_a=a-len(mv.group(0)) if False else ss+mv.start()
        elif m3: label=txt(m3.group(1)); cut_a=ss+m3.start()
        elif m2: label=txt(m2.group(1))
        if mv and m3: pass
        # внутри vlabel может предшествовать h3
        new=out[:cut_a]+out[b:]
        # если секция vtop — переносим и ссылку «подробно», секцию удаляем
        ss2=new.rfind('<section',0,cut_a+1); se2=new.find('</section>',ss2)
        rest=new[ss2:se2+10]
        inner=re.sub(r'^<section[^>]*>|</section>$','',rest)
        mlink=re.fullmatch(r'\s*(<h3[^>]*>.*?</h3>)?\s*(<p[^>]*>\s*<a[^>]*>.*?</a>\s*</p>)?\s*',re.sub(r'<h2[^>]*>.*?</h2>','',inner,flags=re.S),re.S)
        if mlink:
            link=mlink.group(2) or ''
            new=new[:ss2]+new[se2+10:]
        out=new
        items.insert(0,(label,vid,link))
    hp=hero(slug)
    head=''
    if hp: head+=f'<figure class="tophero"><img src="../media/img/{hp}" width="1200" height="800" alt="" decoding="async" fetchpriority="high"></figure>'
    if items:
        t=(T if len(items)>1 else T1)[L]
        head+=f'<section class="vfirst" id="vids_{L}"><h2>{t}</h2>'
        for lab,vid,link in items:
            head+='<div class="vitem">'+(f'<div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{html.escape(lab)}</span></div>' if lab else '')+vid+link+'</div>'
        head+='</section>'
    return head+out
for f in sorted(glob.glob(R+'ops/*.html')):
    slug=os.path.basename(f)[:-5]
    if slug.endswith('-path') or slug=='sitemap': continue
    s=open(f,encoding='utf8').read(); i=s.find('<main>'); j=s.find('</main>')
    main=s[i+6:j]
    parts=re.split(r'(<div data-l="(\w+)">)',main)
    res=parts[0]; k=1
    while k<len(parts):
        tag,L,body=parts[k],parts[k+1],parts[k+2]
        res+=tag+proc(body,L,slug); k+=3
    ns=s[:i+6]+res+s[j:]
    if ns!=s: open(f,'w',encoding='utf8').write(ns); print('ok',slug,ns.count('class="vitem"'))
