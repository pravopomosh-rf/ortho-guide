import sys,glob,html
sys.path.insert(0,sys.argv[1]); from fixes import F,SHARED_RU
apply=sys.argv[2]=='apply'
L=['ru','he','ar','en']
def seg(s,l):
    m=s.find('<main');a=s.find('<div data-l="%s">'%l,m);i=L.index(l)
    b=s.find('<div data-l="%s">'%L[i+1],a) if i<3 else s.find('</main>',a)
    return a,b
miss=[];n=0
files={}
def get(f):
    if f not in files: files[f]=open('ops/%s.html'%f,encoding='utf8').read()
    return files[f]
for f,l,old,new,_ in F:
    s=get(f);a,b=seg(s,l);t=s[a:b]
    o=old.replace('## ','') ; nw=new.replace('## ','')
    c=t.count(o)
    if c==0:
        # try html-escaped quotes
        miss.append((f,l,old));continue
    n+=c; t=t.replace(o,nw); files[f]=s[:a]+t+s[b:]
for p in glob.glob('ops/*.html'):
    f=p[4:-5]
    for l,old,new,_ in SHARED_RU:
        s=get(f);a,b=seg(s,l);t=s[a:b];c=t.count(old)
        if c: n+=c;files[f]=s[:a]+t.replace(old,new)+s[b:]
print('replaced',n);print('MISS',len(miss))
for m in miss: print(m)
if apply:
    for f,s in files.items(): open('ops/%s.html'%f,'w',encoding='utf8').write(s)
