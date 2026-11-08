# finish.sh SRC.mp4 NAME LANG  -> /home/claude/out/NAME_LANG.mp4 + .jpg (сжатие crf25, звук 48к, faststart)
S=$1; N=$2; L=$3; O=/home/claude/out; mkdir -p $O
nice ffmpeg -v error -y -i $S -c:v libx264 -preset medium -crf 25 -pix_fmt yuv420p -threads 1 -c:a aac -b:a 128k -ar 48000 -movflags +faststart $O/${N}_$L.mp4
nice ffmpeg -v error -y -ss 4 -i $O/${N}_$L.mp4 -frames:v 1 -vf scale=720:-1 -q:v 4 $O/${N}_$L.jpg
ls -la $O/${N}_$L.mp4 | awk '{print $5}'
