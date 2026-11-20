#!/usr/bin/env python3
# proc_tts.py FILE.json... : {key: dataURL} -> ttsrepo/aud/<topic>/<lang>/<ID>.opus, F0/cps report, удаляет из todo*.json
import json, base64, sys, os, subprocess, tempfile, numpy as np
R = '/home/claude/ttsrepo'
todo = json.load(open(f'{R}/manus/todo.json')); pri = json.load(open(f'{R}/manus/todo_priority.json'))
CPS = {'ru': (10, 14), 'en': (11, 15), 'he': (8, 11), 'ar': (8, 11)}

def f0(wav):
    x, sr = load(wav)
    fr = int(0.04 * sr); hop = int(0.02 * sr); vals = []
    for i in range(0, len(x) - fr, hop):
        s = x[i:i + fr]
        if np.sqrt(np.mean(s ** 2)) < 0.02: continue
        s = s - s.mean(); ac = np.correlate(s, s, 'full')[fr - 1:]
        lo, hi = int(sr / 300), int(sr / 60)
        j = lo + np.argmax(ac[lo:hi])
        if ac[j] > 0.3 * ac[0]: vals.append(sr / j)
    return float(np.median(vals)) if vals else 0, len(x) / sr

def load(wav):
    raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, 16000

done = []
for f in sys.argv[1:]:
    d = json.load(open(f))
    for k, v in d.items():
        topic, lang, cid = k.split('_', 2)
        txt = todo.get(k) or pri.get(k) or ''
        tmp = tempfile.mktemp(suffix='.wav'); open(tmp, 'wb').write(base64.b64decode(v.split(',', 1)[1]))
        hz, du = f0(tmp); cps = len(txt) / du if du else 0
        lo, hi = CPS[lang]; flag = '' if (80 <= hz <= 160 and lo <= cps <= hi) else '  <-- ПРОВЕРИТЬ'
        out = (f'{R}/aud/{topic}/{lang}/{cid}.opus' if not flag else f'/home/claude/review/{k}.opus'); os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', tmp, '-c:a', 'libopus', '-b:a', '64k', out], check=True)
        os.remove(tmp)
        print(f'{k:22s} {du:5.1f}s F0 {hz:5.0f} cps {cps:4.1f}{flag}')
        if not flag: done.append(k)
        else: print('   (оставлено в todo)')
for k in done: todo.pop(k, None); pri.pop(k, None)
json.dump(todo, open(f'{R}/manus/todo.json', 'w'), ensure_ascii=False, indent=1)
json.dump(pri, open(f'{R}/manus/todo_priority.json', 'w'), ensure_ascii=False, indent=1)
print('принято', len(done), '| todo', len(todo), 'priority', len(pri))
