# python3 mkcues.py spec.json texts.json(lang->id->text) audio_dir_pattern out_prefix  [offset lead]
# audio pattern e.g. /x/aud/hipfx/{lang}/{id}.wav  ({lang}/ empty for ru)
import sys,json,re,unicodedata
sys.path.insert(0,'/home/claude/tools'); from align2 import align
spec=json.load(open(sys.argv[1])); TX=json.load(open(sys.argv[2])); pat=sys.argv[3]; outp=sys.argv[4]
OFF=float(sys.argv[5]) if len(sys.argv)>5 else 0.2; LEAD=float(sys.argv[6]) if len(sys.argv)>6 else 0.1
def norm(w):
    w=unicodedata.normalize('NFC',w).lower()
    w=re.sub('[ً-ْـְٰ-ׇ]','',w)
    w=w.replace('ё','е')
    return re.sub(r'[^\w]','',w)
cache={}
report=[]
for lang in ['ru','he','ar','en']:
    out={}
    for key,(sid,kws) in spec.items():
        kw=kws[lang]; n=1
        if isinstance(kw,list): kw,n=kw
        if (lang,sid) not in cache:
            wav=pat.replace('{lang}/','' if lang=='ru' else lang+'/').replace('{id}',sid)
            cache[(lang,sid)]=align(wav,TX[lang][sid],lang)
        W=cache[(lang,sid)]; k=norm(kw); c=0; hit=None
        for i,(w,a,b) in enumerate(W):
            nw=norm(w)
            if (k==nw) if len(k)<=3 else (k in nw):
                c+=1
                if c==n: hit=(i,a); break
        if hit is None: report.append(f'MISS {lang} {key} {kw}'); continue
        i,a=hit; out[key]=round(a+OFF-LEAD,2)
        ctx=' '.join(x[0] for x in W[max(0,i-2):i+3])
        report.append(f'{lang} {key:12s} {out[key]:6.2f}  …{ctx}…')
    json.dump(out,open(f'{outp}_{lang}.json','w'),ensure_ascii=False,indent=0)
print('\n'.join(report))
