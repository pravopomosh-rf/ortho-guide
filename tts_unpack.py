import json,base64,sys,os,wave
for f in sys.argv[1:]:
    d=json.load(open(f))
    for k,v in d.items():
        topic,key=k.split('/'); lang,cid=key.split('_',1)
        out=f'/home/claude/lam/r/public/aud/{topic}/{lang}/{cid}.wav'
        os.makedirs(os.path.dirname(out),exist_ok=True)
        open(out,'wb').write(base64.b64decode(v.split(',',1)[1]))
        w=wave.open(out); print(k, round(w.getnframes()/w.getframerate(),2))
