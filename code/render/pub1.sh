# pub1.sh TOPIC LANG  → сжатие, vcheck, лист кадров /home/claude/out/sheet_TOPIC_LANG.png
T=$1; L=$2; R=/home/claude/night/lam/r
bash /home/claude/tools/finish.sh $R/out/${T}_$L.mp4 $T $L
python3 /home/claude/tools/vcheck.py /home/claude/out/${T}_$L.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 /home/claude/out/${T}_$L.mp4
TF=$R/src/timing_$T$([ $L = ru ] || echo _$L).json
bash /home/claude/tools/sheet.sh /home/claude/out/${T}_$L.mp4 $TF /home/claude/out/sheet_${T}_$L.png
