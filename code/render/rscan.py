import sys,subprocess,numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import soundfile as sf
enc=VoiceEncoder('cpu')
for f in sys.argv[1:]:
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-ac','1','-ar','16000','/tmp/rs.wav'])
    w,sr=sf.read('/tmp/rs.wav'); win=3*sr; embs=[];ts=[]
    for i in range(0,len(w)-win,win):
        seg=w[i:i+win]
        if np.sqrt((seg**2).mean())<0.01: continue
        embs.append(enc.embed_utterance(preprocess_wav(seg,16000))); ts.append(i/sr)
    E=np.array(embs); c=E.mean(0); c/=np.linalg.norm(c); s=E@c
    bad=[(round(t),round(x,2)) for t,x in zip(ts,s) if x<0.75]
    print(f.split('/')[-1],'min',round(s.min(),2),'med',round(np.median(s),2),'low',bad[:8])
