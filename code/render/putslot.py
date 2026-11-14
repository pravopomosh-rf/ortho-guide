# python3 putslot.py PAGE BASE LANG "Title" — заменяет заглушку video_<lang> (class vdev) на вертикальное видео video/BASE_LANG.mp4 (+jpg); копирует из /home/claude/out
import sys, re, shutil
page, base, L, title = sys.argv[1:5]
R = '/home/claude/ortho-guide/'
shutil.copy(f'/home/claude/out/{base}_{L}.mp4', R + f'video/{base}_{L}.mp4')
shutil.copy(f'/home/claude/out/{base}_{L}.jpg', R + f'video/{base}_{L}.jpg')
lab = {'ru': 'Смотрите видео', 'he': 'צפו בסרטון', 'ar': 'شاهدوا الفيديو', 'en': 'Watch the video'}[L]
p = R + page
s = open(p, encoding='utf8').read()
pat = re.compile(r'<section id="video_' + L + r'" class="vtop[^"]*">.*?</section>', re.S)
new = (f'<section id="video_{L}" class="vtop"><div class="vlabel"><span class="vplay" aria-hidden="true"></span><span>{lab}</span></div>'
       f'<h2>{title}</h2><video class="vid v9" width="1080" height="1920" style="aspect-ratio:1080/1920" controls preload="none" playsinline '
       f'poster="../video/{base}_{L}.jpg" src="../video/{base}_{L}.mp4"></video></section>')
s2, n = pat.subn(new, s, count=1)
assert n == 1, 'slot not found'
open(p, 'w', encoding='utf8').write(s2)
print('ok', page, L)
