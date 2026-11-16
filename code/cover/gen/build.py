import re,html,json,glob,subprocess,os
R='/home/claude/ortho-guide'
L=['ru','he','ar','en']
meta=json.load(open('meta.json'))
cards={k:v for k,v in meta['cards'].items()}
sec=meta['sec']
idx=open(R+'/index.html').read()
def secname(key,l):
    m=re.search(r'id="r_%s_%s"><h2 class="regh">(?:<img[^>]*>)?(.*?)</h2>'%(key,l),idx); return html.unescape(m.group(1))
thr=open(R+'/ops/thr.html').read()
def head(v,l,page=thr):
    i=page.find(f'video/{v}_{l}.mp4'); hs=re.findall(r'<(?:h2|h3)[^>]*>(.*?)</',page[max(0,i-1500):i]); return html.unescape(re.sub('<[^>]+>','',hs[-1]))
def card(v,l):
    c=cards.get(f'{v}|{l}'); return c[0] if c else None
def ant(l):
    return html.unescape(re.search(r'href="ops/thr-anterior.html#lang=%s".*?class="pt">(.*?)</span>'%l,idx).group(1))
# illustration: ('img', path) or ('frame', idx, top)
ILL={'acdf':'p/spine-other.webp','breath':'p/breathing.webp','delir':'p/delirium.webp','falls':'p/falls.webp','fusion':'spine_disc_fusion.svg',
 'kyphoplasty':'vcf.webp','laminectomy':'lami_{l}.webp','logroll':'p/log-roll.webp','osteo':'p/osteosynthesis.webp','pain':'p/pain.webp',
 'postop':'p/postop.webp','preopv':'sec_preop.webp','preop':'sec_preop.webp','press':'p/pressure-sores.webp','shoulder':'p/shoulder-fracture.webp',
 'swell':'p/swelling.webp','drain':'p/drain.webp','dress':'p/dressings.webp','tkr':'tkr_ill.webp','wait':'p/why-wait.webp','walker':'p/walker.webp','ward':'p/after-surgery.webp',
 'wrist':'p/wrist-fracture.webp','ankle':'ankle_anatomy.svg','thr3av':'p/walker.webp','thr2v':'thr_ill.webp'}
FR={'amp':(2,430),'anest':(2,405),'arth':(2,650),'cuff':(0,470),'enox':(5,340),'hipfxv':(1,300),'o2':(0,360),'stairs':(6,470),
 'thr_anterior':(0,950),'pjv':(8.85,440)}
out=[]
for f in sorted(glob.glob(R+'/video/*.mp4')):
    b=os.path.basename(f)[:-4]; v,l=b.rsplit('_',1)
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    tagkey=(sec.get(v,{}).get(l) or [None])[0]
    if v in('thr2v','thr3av','thr3bv','stairs','thr_anterior'): tagkey='hip'
    if v=='preop': tagkey='preop'
    if v in('thr2v','thr3av','thr3bv'):
        h1=card('thr2v',l); sub=head(v,l)
    elif v=='stairs': h1=head(v,l); sub=None
    elif v=='thr_anterior': t=ant(l); h1,sub=t.split(':',1) if ':' in t else (t,None)
    else:
        t=card(v,l)
        if ': ' in t: h1,sub=t.split(': ',1)
        elif ' (' in t and v!='o2': h1,sub=t,None
        else: h1,sub=t,None
    h1=h1.strip(); sub=sub.strip() if sub else None
    if sub: sub=sub[0].upper()+sub[1:]
    ill=ILL.get(v)
    out.append(dict(v=v,l=l,h1=h1,sub=sub,tag=secname(tagkey,l),dur='%d:%02d'%(int(d)//60,int(d)%60),dsec=d,img=ill.replace('{l}',l) if ill else None,fr=FR.get(v)))
json.dump(out,open('data.json','w'),ensure_ascii=False,indent=0)
for o in out:
    if o['l']=='ru': print(o['v'],'|',o['h1'],'|',o['sub'],'|',o['tag'],o['dur'],o['img'] or o['fr'])
print(len(out))
