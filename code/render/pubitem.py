# pubitem.py PAGE BASE LANG "Title" VER — убирает заглушку video_L, ставит ролик ПЕРВЫМ в .vfirst#vids_L
import sys,re,shutil
page,base,L,title,ver=sys.argv[1:6]; R='/home/claude/ortho-guide/'
shutil.copy(f'/home/claude/out/{base}_{L}.mp4',R+f'video/{base}_{L}.mp4')
p=R+page; s=open(p,encoding='utf8').read()
s=re.sub(r'<section id="video_%s" class="vtop vdev">.*?</section>'%L,'',s,count=1,flags=re.S)
if f'video/{base}_{L}.mp4' in s: print('already',L)
else:
    m=re.search(r'(<section class="vfirst" id="vids_%s"><h2>[^<]*</h2>)'%L,s); assert m
    item=(f'<div class="vitem"><div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{title}</span></div>'
          f'<video class="vid v9" width="1080" height="1920" style="aspect-ratio:1080/1920" controls preload="none" playsinline '
          f'poster="../video/c/{base}_{L}.jpg?v={ver}" src="../video/{base}_{L}.mp4?v={ver}"></video></div>')
    s=s[:m.end()]+item+s[m.end():]; print('ok',L)
open(p,'w',encoding='utf8').write(s)
