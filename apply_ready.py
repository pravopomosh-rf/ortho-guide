# применяет перевод ко всем страницам, где все строки уже есть в tm.json и амхарского ещё нет
import sys,json,glob,os,re; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import amtool
W=os.path.dirname(os.path.abspath(__file__)); os.chdir(amtool.ROOT)
tm=json.load(open(W+'/tm.json'))
# добавить ответы ChatGPT: python3 apply_ready.py add bNN gpt.txt
if len(sys.argv)>3 and sys.argv[1]=='add':
    en=json.load(open(W+'/b/%s_en.json'%sys.argv[2])); t=open(sys.argv[3]).read()
    d={int(m.group(1)):m.group(2).strip() for m in re.finditer(r'^(\d{3})\t(.+)$',t,re.M)}
    miss=[i for i in range(1,len(en)+1) if i not in d]; assert not miss,miss
    for i,s in enumerate(en,1): tm[s]=d[i]
    json.dump(tm,open(W+'/tm.json','w'),ensure_ascii=False,indent=0); print('tm',len(tm))
for f in sorted(glob.glob('ops/*.html')):
    s=open(f).read()
    if 'data-l="am"' in s: continue
    ex=amtool.extract(f)
    if all(x in tm for x in ex): amtool.apply(f,[tm[x] for x in ex]); print('applied',f)
