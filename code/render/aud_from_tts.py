import json,subprocess,sys,os
topic=sys.argv[1]; langs=sys.argv[2:] or ['ru','he','ar','en']
R='/home/claude/night/lam/r'; T='/home/claude/ttsrepo'
tx=json.load(open(f'{T}/{topic}.json'))
os.makedirs(f'{R}/public/aud',exist_ok=True)
for L in langs:
    tf=f'{R}/src/timing_{topic}'+('' if L=='ru' else '_'+L)+'.json'
    tm=json.load(open(tf)); ch=0
    for x in tm:
        src=f'{T}/aud/{topic}/{L}/{x["id"]}.opus'; out=f'{topic}_{L}_{x["id"]}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-ar','48000','-ac','2',f'{R}/public/aud/{out}'],check=True)
        d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{R}/public/aud/{out}']))
        x['dur']=round(d,2); x['audio']=out
        t=tx.get(f'{L}_{x["id"]}')
        if t and t.strip()!=x['text'].strip(): ch+=1; x['text']=t.strip()
    json.dump(tm,open(tf,'w'),ensure_ascii=False)
    print(L,len(tm),'clips; text updated',ch,'; total s',round(sum(x['dur']+0.5 for x in tm),1))
