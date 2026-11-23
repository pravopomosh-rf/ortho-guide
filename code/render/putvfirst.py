# putvfirst.py PAGE BASE "ru title|he|ar|en" LANGS... — заглушку video_L (vtop vdev) заменить на section.vfirst перед key_L
import sys,re,shutil
page,base,titles=sys.argv[1:4]; langs=sys.argv[4:]
T=dict(zip(['ru','he','ar','en'],titles.split('|')))
H={'ru':'Сначала посмотрите видео','he':'קודם כל, צפו בסרטון','ar':'أولًا، شاهدوا الفيديو','en':'Start with the video'}
R='/home/claude/ortho-guide/'; p=R+page; s=open(p,encoding='utf8').read()
for L in langs:
    shutil.copy(f'/home/claude/out/{base}_{L}.mp4',R+f'video/{base}_{L}.mp4')
    s=re.sub(r'<section id="video_%s" class="vtop vdev">.*?</section>'%L,'',s,count=1,flags=re.S)
    if f'id="vids_{L}"' in s: print('vfirst exists',L); continue
    sec=(f'<section class="vfirst" id="vids_{L}"><h2>{H[L]}</h2><div class="vitem"><div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{T[L]}</span></div>'
         f'<video class="vid v9" width="1080" height="1920" style="aspect-ratio:1080/1920" controls preload="none" playsinline poster="../video/c/{base}_{L}.jpg" src="../video/{base}_{L}.mp4?v=2311a"></video></div></section>')
    k=f'<section class="key" id="key_{L}">'; assert k in s; s=s.replace(k,sec+k,1); print('ok',L)
open(p,'w',encoding='utf8').write(s)
