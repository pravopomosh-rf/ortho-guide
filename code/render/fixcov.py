# fixcov.py BASE L... — постер c/, карточки t/ 800x600
import sys,glob,re
b=sys.argv[1]; R='/home/claude/ortho-guide/'
for f in [R+'index.html']+glob.glob(R+'ops/*.html'):
    s=open(f,encoding='utf8').read(); o=s
    for L in sys.argv[2:]:
        s=s.replace(f'poster="../video/{b}_{L}.jpg"',f'poster="../video/c/{b}_{L}.jpg"')
        s=re.sub(r'src="((?:\.\./)?)video/'+b+'_'+L+r'\.jpg" width="720" height="1280"',lambda m:f'src="{m.group(1)}video/t/{b}_{L}.jpg" width="800" height="600"',s)
    if s!=o: open(f,'w',encoding='utf8').write(s); print('fixed',f.split('/')[-1])
