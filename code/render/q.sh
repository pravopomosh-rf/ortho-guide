#!/bin/bash
# usage: q.sh Comp:out ...
cd /home/claude/night/lam/r
for a in "$@"; do c=${a%%:*}; o=${a##*:}
  echo "$(date +%T) START $c" >> /tmp/q.log
  npx remotion render src/index.ts $c out/$o.mp4 --concurrency=2 --crf=20 --browser-executable=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome >/tmp/r_$o.log 2>&1 && echo "$(date +%T) DONE $c" >> /tmp/q.log || echo "$(date +%T) FAIL $c" >> /tmp/q.log
done
