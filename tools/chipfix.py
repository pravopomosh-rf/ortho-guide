#!/usr/bin/env python3
"""Карточки-ссылки с бейджем «Памятка/Read/…», хотя у страницы-цели на этом языке уже есть видео.
python3 tools/chipfix.py          — показать
python3 tools/chipfix.py --apply  — заменить бейдж на «▶ Видео» (class="chip v")"""
import os,re,sys,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));os.chdir(ROOT)
LB=re.compile(r'<div data-l="(ru|he|ar|en|am)">')
VID={'ru':'▶ Видео','he':'▶ סרטון','ar':'▶ فيديو','en':'▶ Video','am':'▶ ቪዲዮ'}
CARD=re.compile(r'(<a [^>]*href="([^"#?]+\.html)[^"]*"[^>]*>(?:(?!</a>).)*?)<span class="chip">([^<]*)</span>',re.S)
def langs_with_video(path):
    s=open(path,encoding='utf-8').read();marks=[(m.start(),m.group(1)) for m in LB.finditer(s)]
    def L(pos):
        p=[l for q,l in marks if q<pos];return p[-1] if p else None
    has={L(m.start()) for m in re.finditer(r'<video\b',s)}
    soon={L(m.start()) for m in re.finditer(r'class="vsoon"',s)}
    return has,soon
cache={};tot=0
for p in sorted(glob.glob('**/*.html',recursive=True)):
    s=open(p,encoding='utf-8').read();marks=[(m.start(),m.group(1)) for m in LB.finditer(s)]
    out=[];last=0;n=0
    for m in CARD.finditer(s):
        prev=[l for q,l in marks if q<m.start()];lang=prev[-1] if prev else None
        tgt=os.path.normpath(os.path.join(os.path.dirname(p),m.group(2)))
        if lang not in VID or lang=='am' or not os.path.exists(tgt):continue
        if tgt not in cache:cache[tgt]=langs_with_video(tgt)
        has,soon=cache[tgt]
        if lang in has and lang not in soon:
            print(f'{p} [{lang}] → {m.group(2)}: «{m.group(3)}»');n+=1
            out.append(s[last:m.start()]+m.group(1)+f'<span class="chip v">{VID[lang]}</span>');last=m.end()
    if n and '--apply' in sys.argv:
        open(p,'w',encoding='utf-8').write(''.join(out)+s[last:])
    tot+=n
print('итого',tot)
