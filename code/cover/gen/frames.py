import json,subprocess
D=json.load(open('data.json'))
for o in D:
    if not o['fr']: continue
    i,top=o['fr']; t=o['dsec']*(0.05+0.09*i)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f"/home/claude/ortho-guide/video/{o['v']}_{o['l']}.mp4",'-frames:v','1','-vf',f'scale=1080:1920,crop=1080:788:0:{top}',f"ill/{o['v']}_{o['l']}.png"])
