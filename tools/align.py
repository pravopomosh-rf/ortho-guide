# Точное время слов по известному тексту: паузы (ffmpeg silencedetect) + пропорция по буквам.
# python3 align.py file.wav "текст" [json_out]  -> [[word, start, end], ...]
import sys,re,json,subprocess
def pauses(wav,noise=-38,d=0.06):
    o=subprocess.run(['ffmpeg','-i',wav,'-af',f'silencedetect=noise={noise}dB:d={d}','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',o)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',o)]
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav]).decode())
    if len(en)<len(st): en.append(dur)
    return list(zip(st,en)),dur
def align(wav,text):
    P,dur=pauses(wav)
    s0=P[0][1] if P and P[0][0]<0.05 else 0.0
    e0=P[-1][0] if P and P[-1][1]>=dur-0.05 else dur
    inner0=[p for p in P if p[0]>s0+0.05 and p[1]<e0-0.05]
    inner=[]
    for p in inner0:
        if inner and p[0]-inner[-1][1]<0.06: inner[-1]=(inner[-1][0],p[1])
        else: inner.append(p)
    words=text.split()
    wl=[max(1,len(re.sub(r'[^\w]','',w))) for w in words]
    # границы фраз = слова с пунктуацией на конце
    B=[i for i,w in enumerate(words[:-1]) if re.search(r'[,.;:!?—–،؛؟]$',w) or words[i+1] in ('—','–')]
    tot=sum(wl); speech=e0-s0-sum(b-a for a,b in inner)
    def s2r(x):  # время «чистой речи» -> реальное время (с паузами)
        t=s0+x
        for a,b in inner:
            if a<t: t+=b-a
        return t
    def est(i): return s2r((sum(wl[:i+1])/tot)*speech)
    rate=tot/max(0.5,speech)  # букв в секунду речи
    m=[]; aw,at=0,s0; k0=0
    for i in range(len(B)):
        ch=sum(wl[aw:B[i]+1]); e=ch/rate
        # оценка конца слова B[i] с учётом пауз после якоря
        def real_end(t,e):
            for pa,pb in inner[k0:]:
                if pa<t+e and pa>=t: e+=0  # паузы внутри фразы считаем частью речи (короткие)
            return t+e
        est_end=real_end(at,e)
        best=None
        for k in range(k0,len(inner)):
            pa,pb=inner[k]
            if pa<at: continue
            d=abs(pa-est_end)
            if pa>est_end+1.5: break
            sc=d-min(0.25,(pb-pa))*0.8
            if best is None or sc<best[0]: best=(sc,k,d)
        tol=0.35+0.25*e
        if best and best[2]<=tol:
            k=best[1]; m.append((i,k)); aw,at=B[i]+1,inner[k][1]; k0=k+1
        else: m.append((i,None))
    # якорные точки: (индекс слова начала фразы, время)
    anchors=[(0,s0)]; ends={}
    for i,k in m:
        if k is not None: anchors.append((B[i]+1,inner[k][1])); ends[B[i]]=inner[k][0]
    anchors.append((len(words),e0))
    out=[]
    for a in range(len(anchors)-1):
        (w0,t0),(w1,t1)=anchors[a],anchors[a+1]
        tend=ends.get(w1-1,t1)
        L=sum(wl[w0:w1]) or 1; acc=0
        for w in range(w0,w1):
            st=t0+(acc/L)*(tend-t0); acc+=wl[w]; en=t0+(acc/L)*(tend-t0)
            out.append([words[w],round(st,3),round(en,3)])
    return out
if __name__=='__main__':
    r=align(sys.argv[1],sys.argv[2])
    if len(sys.argv)>3: json.dump(r,open(sys.argv[3],'w'),ensure_ascii=False)
    else: print(json.dumps(r,ensure_ascii=False))
