Рендер роликов тем (восстановление 14.11): night_code_07-11n + code_* (см. handoff) → /home/claude/night/lam/r; tools → /home/claude/tools.
1) python3 aud_from_tts.py TOPIC [langs]  (opus из aud/ → public/aud, dur/audio/text в timing)
2) q.sh Comp:topic_lang ...   (лог /tmp/q.log, ~10–13 мин на ролик)
3) pub1.sh TOPIC LANG  (сжатие, vcheck, лист кадров) → putslot.py PAGE BASE LANG "Заголовок" → linkvid.py PAGE BASE langs... → commit/push main
