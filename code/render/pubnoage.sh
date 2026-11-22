# pubnoage.sh FILE PAGE LANG  — cp out → video/, ?v=2111n
F=$1; P=$2; L=$3; cd /home/claude/ortho-guide
cp /home/claude/out/${F}_$L.mp4 video/${F}_$L.mp4 && cp /home/claude/out/${F}_$L.jpg video/${F}_$L.jpg
python3 - "$F" "$L" "$P" <<'P'
import re,sys
f,l,p=sys.argv[1:]
s=open('ops/'+p).read()
n=re.subn(r'(video/%s_%s\.(?:mp4|jpg))(\?v=[A-Za-z0-9]+)?'%(f,l),r'\1?v=2111n',s)
open('ops/'+p,'w').write(n[0]);print('refs',n[1])
P
git add video/${F}_$L.mp4 video/${F}_$L.jpg ops/$P && git commit -qm "Ролик $F ($L): сцена 1 без возраста пациента, перерендер; vcheck — замечаний нет

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VMoax7PNAi4Dx2XVMd2BWq" && git push -q origin HEAD:refs/heads/main && git log --oneline -1
