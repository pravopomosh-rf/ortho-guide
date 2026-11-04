import re,os,sys
S='/tmp/claude-0/-home-claude/8cf9b33d-31b0-588b-8719-e4ac2d5ecf3d/scratchpad/en/'
def block(s,start):
  depth=0
  for m in re.finditer(r'<(/?)div\b[^>]*>',s[start:]):
    depth+= -1 if m.group(1) else 1
    if depth==0: return start+m.end()
done=[]
for n in sorted(os.listdir(S+'out')):
  if not n.endswith('.main.html'): continue
  page=n[:-len('.main.html')]; f=page.replace('__','/')
  h=open(S+'out/'+page+'.header.html').read(); m=open(S+'out/'+n).read()
  assert h.startswith('<div data-l="en">') and m.startswith('<div data-l="en">'),page
  s=open(f).read()
  if 'data-l="en"><' in s.split('<main')[1][:40] or s.count('<div data-l="en">')>=2: print('skip',f);continue
  # header: after ar block inside header
  a=s.index('<div data-l="ar">',s.index('<header')); e=block(s,a); s=s[:e]+h+s[e:]
  a=s.index('<div data-l="ar">',s.index('<main')); e=block(s,a); s=s[:e]+m+s[e:]
  open(f,'w').write(s); done.append(f)
print('merged',done)
