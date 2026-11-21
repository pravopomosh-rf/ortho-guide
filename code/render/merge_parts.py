#!/usr/bin/env python3
# merge_parts.py OUT.json IN.json... : склейка ключей "k|iofn" с паузой 0.35 с; неполные части -> /home/claude/stg/parts/
import json,sys,base64,subprocess,os,glob,tempfile
P='/home/claude/stg/parts'; os.makedirs(P,exist_ok=True)
out={}
for f in sys.argv[2:]:
    for k,v in json.load(open(f)).items():
        if '|' in k: open(f'{P}/{k}.b64','w').write(v)
        else: out[k]=v
groups={}
for p in glob.glob(P+'/*.b64'):
    k,part=os.path.basename(p)[:-4].split('|'); i,n=part.split('of'); groups.setdefault(k,{})[int(i)]=(p,int(n))
for k,g in groups.items():
    n=list(g.values())[0][1]
    if len(g)<n: print('неполно',k,len(g),n); continue
    d=tempfile.mkdtemp(); lst=[]
    for i in range(1,n+1):
        raw=base64.b64decode(open(g[i][0]).read().split(',',1)[1]); w=f'{d}/{i}.wav'; open(w+'.in','wb').write(raw)
        subprocess.run(['ffmpeg','-v','error','-y','-i',w+'.in','-ar','24000','-ac','1',w],check=True); lst.append(w)
        if i<n:
            s=f'{d}/s{i}.wav'; subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','anullsrc=r=24000:cl=mono','-t','0.35',s],check=True); lst.append(s)
    open(d+'/l.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',d+'/l.txt','-c:a','pcm_s16le',d+'/all.wav'],check=True)
    out[k]='data:audio/wav;base64,'+base64.b64encode(open(d+'/all.wav','rb').read()).decode()
    for i in g: os.remove(g[i][0])
    print('склеено',k,n)
json.dump(out,open(sys.argv[1],'w'))
