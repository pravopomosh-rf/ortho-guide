import sys,json,glob,os; sys.path.insert(0,'/home/claude/amw'); import amtool
os.chdir('/home/claude/ortho-guide')
tm=json.load(open('/home/claude/amw/tm.json'))
pr=['preop','admission','thr','tkr','hip-fracture','after-surgery','pain','postop','drain','dressings','enoxaparin-injections','falls','walker','breathing','swelling','delirium','pressure-sores','after-anaesthesia','oxygen-sleep','rehab','thr-home','why-wait','cpe-vre','log-roll','knee-arthroscopy','osteosynthesis','ankle-fracture','achilles-repair','wrist-fracture','shoulder-fracture','rotator-cuff','shoulder-replacement','laminectomy','fusion-discectomy','kyphoplasty','spine-other','durotomy','thr-anterior','amputation','diabetic-foot','cellulitis','purulent-infection']
allp=[os.path.basename(f)[:-5] for f in glob.glob('ops/*.html')]
rest=[p for p in allp if p not in pr and not p.endswith('-path') and p!='sitemap']
print('not in order:',rest)
seen=set(tm); batches=[]; cur=[]; size=0; LIM=7000
for p in pr:
    for t in amtool.extract('ops/%s.html'%p):
        if t in seen: continue
        seen.add(t)
        if size+len(t)>LIM and cur: batches.append(cur); cur=[]; size=0
        cur.append(t); size+=len(t)
if cur: batches.append(cur)
os.makedirs('/home/claude/amw/b',exist_ok=True)
head=open('/home/claude/amw/head.txt').read()
for i,b in enumerate(batches,2):
    json.dump(b,open('/home/claude/amw/b/b%02d_en.json'%i,'w'),ensure_ascii=False,indent=0)
    open('/home/claude/amw/b/am_b%02d_check.txt'%i,'w').write(head.replace('{B}','%02d'%i)+'\n'.join('%03d\t%s'%(k+1,t) for k,t in enumerate(b))+'\n')
print(len(batches),[sum(map(len,b)) for b in batches][:5])
