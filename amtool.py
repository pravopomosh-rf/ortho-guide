import re,sys,json,os,html
ROOT='/home/claude/ortho-guide'
def blocks(s):
    """return list of (start,end) of EN elements: header div, pv span, main div"""
    out=[]
    for m in re.finditer(r'<(div|span) data-l="en">',s):
        tag=m.group(1); i=m.start(); depth=0; pos=i
        pat=re.compile(r'<(/?)%s\b[^>]*>'%tag)
        for t in pat.finditer(s,i):
            depth+= -1 if t.group(1) else 1
            if depth==0: out.append((i,t.end())); break
    return out
TXT=re.compile(r'(<[^>]+>)')
def segs(chunk):
    parts=TXT.split(chunk); res=[]
    skip=False
    for k,p in enumerate(parts):
        if p.startswith('<'):
            low=p.lower()
            if low.startswith('<script') or low.startswith('<style'): skip=True
            if low.startswith('</script') or low.startswith('</style'): skip=False
            continue
        if not skip and re.search(r'[A-Za-z]',p): res.append(k)
    return parts,res
def extract(page):
    s=open(os.path.join(ROOT,page),encoding='utf-8').read()
    out=[]
    for a,b in blocks(s):
        parts,idx=segs(s[a:b])
        for k in idx: out.append(html.unescape(parts[k].strip()))
    return out
def apply(page,tr,hevideo=True):
    p=os.path.join(ROOT,page); s=open(p,encoding='utf-8').read()
    assert 'data-l="am"' not in s, 'already'
    bl=blocks(s); n=0; new=s; off=0
    for a,b in bl:
        parts,idx=segs(s[a:b])
        for k in idx:
            raw=parts[k]; lead=raw[:len(raw)-len(raw.lstrip())]; tail=raw[len(raw.rstrip()):]
            parts[k]=lead+html.escape(tr[n],quote=False)+tail; n+=1
        am=''.join(parts)
        am=am.replace('data-l="en"','data-l="am"',1)
        am=re.sub(r'(id|href|for|aria-controls|aria-labelledby)="([^"]*?)_en(\b[^"]*)"',lambda m:f'{m.group(1)}="{m.group(2)}_am{m.group(3)}"',am)
        am=re.sub(r'(href="[^"]*#[^"]*)lang=en',r'\1lang=am',am)
        am=am.replace("setL('en')","setL('am')")
        if hevideo:
            def sw(m):
                f=m.group(2); g=f.replace('_en.','_he.')
                rel=os.path.normpath(os.path.join(os.path.dirname(p),g.split('?')[0]))
                return m.group(1)+(g if os.path.exists(rel) else f)+'"'
            am=re.sub(r'((?:src|poster)=")([^"]*_en\.(?:mp4|jpg|webp)[^"]*)"',sw,am)
        new=new[:b+off]+am+new[b+off:]; off+=len(am)
    assert n==len(tr),(n,len(tr))
    open(p,'w',encoding='utf-8').write(new)
if __name__=='__main__':
    if sys.argv[1]=='ex':
        for page in sys.argv[2:]:
            x=extract(page); print(page,len(x),sum(len(t) for t in x))
