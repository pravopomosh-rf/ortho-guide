# putpjv.py LANG "Title" — вставляет секцию pjv_<lang> с роликом перед pjq_<lang> в tkr.html и thr.html
import sys,re
L,title=sys.argv[1],sys.argv[2]
for pg in ['tkr.html','thr.html']:
    p='/home/claude/ortho-guide/ops/'+pg; s=open(p,encoding='utf8').read()
    if f'id="pjv_{L}"' in s: s=re.sub(r'<section id="pjv_'+L+r'">.*?</section>','',s,count=1,flags=re.S)
    new=(f'<section id="pjv_{L}"><h2>{title}</h2><video class="vid v9" width="1080" height="1920" style="aspect-ratio:1080/1920" controls preload="none" playsinline '
         f'poster="../video/c/pjv_{L}.jpg" src="../video/pjv_{L}.mp4"></video></section>')
    k=s.find(f'<section id="pjq_{L}">'); assert k>0
    s=s[:k]+new+s[k:]; open(p,'w',encoding='utf8').write(s); print('ok',pg,L)
