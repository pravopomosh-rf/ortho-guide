# Нормализует все <video> на страницах: размеры кадра (нет "схлопывания"), класс vid, preload=none
import re,glob,subprocess,os,sys
R=sys.argv[1] if len(sys.argv)>1 else '.'
dims={}
def dim(p):
    if p not in dims:
        o=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip().strip(',').split(',')
        dims[p]=(int(o[0]),int(o[1])) if len(o)>=2 and o[0] else None
    return dims[p]
n=0
for f in glob.glob(R+'/ops/*.html')+[R+'/index.html']:
    s=open(f,encoding='utf-8').read()
    def fx(m):
        global n
        t=m.group(0)
        if 'class="hero' in t or 'hero' in t.split('src')[0]: return t
        sm=re.search(r'src="([^"]+\.mp4)"',t)
        if not sm: return t
        p=os.path.normpath(os.path.join(os.path.dirname(f),sm.group(1)))
        d=dim(p) if os.path.exists(p) else None
        if not d: return t
        w,h=d
        t=re.sub(r'\s(width|height)="\d+"','',t)
        t=re.sub(r'\sstyle="[^"]*"','',t)
        t=re.sub(r'\sclass="[^"]*"','',t)
        cls='vid v9' if h>w else 'vid v16'
        t=t.replace('<video','<video class="%s" width="%d" height="%d" style="aspect-ratio:%d/%d"'%(cls,w,h,w,h),1)
        n+=1
        return t
    s2=re.sub(r'<video\b[^>]*>',fx,s)
    if s2!=s: open(f,'w',encoding='utf-8').write(s2)
print('videos fixed',n)
