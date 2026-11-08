# Авто-разметка окон для вертикали из широкого ролика.
# python3 autocam.py wide.mp4 scenes.json out.json   (scenes.json: [[id,start,dur],...] в сек)
import sys,json,subprocess,numpy as np
mp4,scj,outj=sys.argv[1:4]
W,H,S=480,270,4.0   # 1920/480
FPSX=4
raw=subprocess.run(['ffmpeg','-v','error','-i',mp4,'-vf',f'fps={FPSX},scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.int16)
bg=np.median(fr[::7],axis=0)
import os
Y0,Y1=int(float(os.environ.get('AC_Y0',228))/S),int(float(os.environ.get('AC_Y1',850))/S)
SINGLE=os.environ.get('AC_SINGLE')=='1'   # полоса контента (без заголовка и субтитров)
def ink(i):
    d=np.abs(fr[i]-bg).max(axis=2)
    m=(d>40)
    m[:Y0]=0;m[Y1:]=0
    return m
sc=json.load(open(scj))
out={}
def bbox(m,x0,x1):
    sub=m[:,x0:x1]
    ys=np.where(sub.any(1))[0];xs=np.where(sub.any(0))[0]
    if len(ys)==0: return None
    return [x0+xs[0],ys[0],x0+xs[-1]+1,ys[-1]+1]
for sid,a,d in sc:
    i0=int(a*FPSX)+1;i1=int((a+d)*FPSX)-1
    ms=[ink(i) for i in range(i0,min(i1,len(fr)))]
    def split_of(m):
        if SINGLE: return None
        col=m.sum(0)
        cand=[x for x in range(int(560/S),int(1360/S)) if col[max(0,x-3):x+4].max()<=3]
        if not cand: return None
        runs=[];st=cand[0];pv=cand[0]
        for x in cand[1:]:
            if x!=pv+1: runs.append((st,pv));st=x
            pv=x
        runs.append((st,pv));r=max(runs,key=lambda r:r[1]-r[0])
        return (r[0]+r[1])//2
    # мгновенная маска, расширенная по времени на ±0.75 с
    inst=[]
    for q in range(len(ms)):
        m=ms[q].copy()
        for z in range(max(0,q-3),min(len(ms),q+4)): m|=ms[z]
        inst.append(m)
    phases=[];k=0
    while k<len(inst):
        acc=inst[k].copy();sp=split_of(acc);j=k+1
        while j<len(inst):
            ns=split_of(inst[j])
            if (sp is None)!=(ns is None): break
            if sp is not None:
                u=acc|inst[j];us=split_of(u)
                if us is None or abs(us-sp)>25: break
                acc=u;sp=us
            else:
                acc=acc|inst[j]
            j+=1
        phases.append((k,j,acc,sp));k=j
    # сливаем слишком короткие фазы (<1.5 с) с соседними
    ph=[]
    for p in phases:
        if ph and (p[1]-p[0])<1.5*FPSX:
            k0,_,acc,sp0=ph[-1]
            ph[-1]=(k0,p[1],acc,sp0)
            continue
        ph.append(p)
    res=[]
    for k0,k1,acc,sp in ph:
        if sp is not None:
            # проверим разрез ещё раз на объединении
            col=acc.sum(0)
            if col[max(0,sp-2):sp+3].max()>3*max(1,(k1-k0)): sp=None
        pad=6
        if sp is None:
            b=bbox(acc,0,W)
            rects=[b] if b else []
        else:
            rects=[r for r in (bbox(acc,0,sp),bbox(acc,sp,W)) if r]
        R=[]
        for x0,y0,x1,y1 in rects:
            x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(W,x1+pad);y1=min(H,y1+pad)
            R.append([int(x0*S),int(y0*S),int((x1-x0)*S),int((y1-y0)*S)])
        res.append({'t':round(k0/FPSX,2),'p':R})
    out[sid]=res
json.dump(out,open(outj,'w'))
for k,v in out.items(): print(k,[(x['t'],len(x['p'])) for x in v])
