# Replace wide video NAME_LANG with vertical NEWNAME_LANG on all pages. Usage: vswap.py thr2 thr2v ru
import sys, re, glob, os, shutil
old, new, L = sys.argv[1:4]
os.chdir('/home/claude/ortho-guide')
shutil.copy(f'/home/claude/out/{new}_{L}.mp4', f'video/{new}_{L}.mp4'); shutil.copy(f'/home/claude/out/{new}_{L}.jpg', f'video/{new}_{L}.jpg')
ST = 'style="display:block;margin:0 auto;width:auto;max-width:100%;max-height:80vh"'
n = 0
for p in glob.glob('*.html') + glob.glob('ops/*.html'):
    s = open(p, encoding='utf8').read()
    pat = re.compile(r'<video([^>]*?)poster="(\.\./)?video/' + old + '_' + L + r'\.jpg" src="(\.\./)?video/' + old + '_' + L + r'\.mp4"([^>]*)>')
    def rep(m):
        pre = m.group(2) or ''; rest = re.sub(r'\s*style="[^"]*"', '', m.group(4))
        return f'<video{m.group(1)}poster="{pre}video/{new}_{L}.jpg" src="{pre}video/{new}_{L}.mp4"{rest} {ST}>'
    s2, k = pat.subn(rep, s)
    if k: open(p, 'w', encoding='utf8').write(s2); n += k
print('replaced', n)
assert n > 0
left = [p for p in glob.glob('*.html') + glob.glob('ops/*.html') if f'{old}_{L}.mp4' in open(p, encoding='utf8').read()]
if not left:
    for e in ['mp4', 'jpg']:
        if os.path.exists(f'video/{old}_{L}.{e}'): os.remove(f'video/{old}_{L}.{e}')
    print('old removed')
else: print('old still used in', left)
