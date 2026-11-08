# Точное время слов: Whisper (word timestamps, подсказка = точный текст) + сопоставление со сценарием + уточнение по паузам.
import re,json,os,subprocess,hashlib,difflib,unicodedata,sys
sys.path.insert(0,'/home/claude/tools')
from align import pauses
MODEL='/home/claude/wm/ggml-base.bin'
CACHE='/home/claude/wm/cache'; os.makedirs(CACHE,exist_ok=True)
_m=None
def norm(w):
    w=unicodedata.normalize('NFC',w).lower()
    w=re.sub('[ً-ْـְٰ-ׇ]','',w).replace('ё','е')
    return re.sub(r'[^\w]','',w)
def whisper(wav,lang,prompt):
    h=hashlib.md5((open(wav,'rb').read()[:2000000].hex()[:4000]+lang+prompt).encode()).hexdigest()
    cp=f'{CACHE}/{h}.json'
    if os.path.exists(cp): return json.load(open(cp))
    global _m
    from pywhispercpp.model import Model
    import tempfile
    tmp=tempfile.mktemp(suffix='.wav'); subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-ar','16000','-ac','1',tmp],check=True)
    if _m is None: _m=Model(MODEL,n_threads=2,print_progress=False,print_realtime=False)
    segs=_m.transcribe(tmp,language=lang,token_timestamps=True,max_len=1,split_on_word=True,initial_prompt=prompt[:800])
    r=[[s.t0/100,s.t1/100,s.text.strip()] for s in segs if s.text.strip()]
    json.dump(r,open(cp,'w'),ensure_ascii=False); return r
def align(wav,text,lang):
    W=text.split(); wn=[norm(w) for w in W]
    R=whisper(wav,lang,''); rn=[norm(x[2]) for x in R]
    P,dur=pauses(wav)
    sm=difflib.SequenceMatcher(None,wn,rn,autojunk=False)
    st=[None]*len(W)
    for a,b,n in sm.get_matching_blocks():
        for k in range(n): st[a+k]=R[b+k][0]
    # частичные совпадения внутри replace-блоков: по позиции
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='replace' and (i2-i1)==(j2-j1):
            for k in range(i2-i1): st[i1+k]=R[j1+k][0]
    # интерполяция пропусков
    known=[(i,t) for i,t in enumerate(st) if t is not None]
    if not known: return [[w,0,0] for w in W]
    for i in range(len(W)):
        if st[i] is None:
            prev=[k for k in known if k[0]<i]; nxt=[k for k in known if k[0]>i]
            if prev and nxt:
                (i0,t0),(i1,t1)=prev[-1],nxt[0]; st[i]=t0+(t1-t0)*(i-i0)/(i1-i0)
            elif prev: st[i]=prev[-1][1]+0.35*(i-prev[-1][0])
            else: st[i]=max(0,nxt[0][1]-0.35*(nxt[0][0]-i))
    # уточнение: если слово стоит после пунктуации и рядом (±0.45с) есть конец паузы — берём его
    ends=[b for a,b in P if b<dur-0.05]
    for i in range(1,len(W)):
        if re.search(r'[,.;:!?—–،؛؟]$',W[i-1]) or W[i-1] in ('—','–'):
            c=[e for e in ends if abs(e-st[i])<0.45]
            if c: st[i]=min(c,key=lambda e:abs(e-st[i]))
    return [[W[i],round(st[i],3),None] for i in range(len(W))]
