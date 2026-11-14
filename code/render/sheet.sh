# sheet.sh VIDEO TIMING OUT — кадр в середине каждой сцены, сетка 6 колонок
V=$1; T=$2; O=$3; D=$(mktemp -d)
python3 - "$T" > $D/ts <<'P'
import json,sys
t=json.load(open(sys.argv[1])); s=0.13
for x in t: print(round(s+x['dur']*0.6,2)); s+=x['dur']+0.5
P
i=0; for ts in $(cat $D/ts); do i=$((i+1)); ffmpeg -v error -y -ss $ts -i $V -frames:v 1 -vf "scale=300:-1,drawtext=text='$i  ${ts}s':x=8:y=8:fontsize=22:fontcolor=red:box=1:boxcolor=white" $D/f$(printf %02d $i).png; done
ffmpeg -v error -y -pattern_type glob -i "$D/f*.png" -vf "tile=6x$(( (i+5)/6 )):padding=6:color=gray" -frames:v 1 $O
echo $O
