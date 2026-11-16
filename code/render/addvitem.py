# addvitem.py PAGE BASE LANG "Title" — добавляет видео в блок .vfirst#vids_LANG (в конец), копирует mp4 из /home/claude/out
import sys, re, shutil
page, base, L, title = sys.argv[1:5]
R = '/home/claude/ortho-guide/'
shutil.copy(f'/home/claude/out/{base}_{L}.mp4', R + f'video/{base}_{L}.mp4')
p = R + page; s = open(p, encoding='utf8').read()
if f'video/{base}_{L}.mp4' in s: print('already', L); sys.exit()
m = re.search(r'<section class="vfirst" id="vids_' + L + r'">.*?</section>', s, re.S)
assert m, 'no vfirst'
item = (f'<div class="vitem"><div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{title}</span></div>'
        f'<video class="vid v9" width="1080" height="1920" style="aspect-ratio:1080/1920" controls preload="none" playsinline '
        f'poster="../video/c/{base}_{L}.jpg" src="../video/{base}_{L}.mp4"></video></div>')
blk = m.group(0); nb = blk[:-len('</section>')] + item + '</section>'
s = s[:m.start()] + nb + s[m.end():]
open(p, 'w', encoding='utf8').write(s); print('ok', L)
