# pubfix.sh FILE PAGE LANG VER MSG
F=$1; P=$2; L=$3; V=$4; M=$5; cd /home/claude/ortho-guide
git fetch -q origin main && git checkout -q -B work origin/main
cp /home/claude/out/${F}_$L.mp4 video/${F}_$L.mp4 && cp /home/claude/out/${F}_$L.jpg video/${F}_$L.jpg
python3 - "$F" "$L" "$P" "$V" <<'P'
import re,sys
f,l,p,v=sys.argv[1:]
s=open('ops/'+p).read()
n=re.subn(r'(video/%s_%s\.(?:mp4|jpg))(\?v=[A-Za-z0-9]+)?'%(f,l),r'\1?v='+v,s)
open('ops/'+p,'w').write(n[0]);print('refs',n[1])
P
git add video/${F}_$L.mp4 video/${F}_$L.jpg ops/$P && git commit -qm "$M

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VMoaxB76jp1V5jrWP2sKy7" && git push -q origin HEAD:refs/heads/main && git log --oneline -1
