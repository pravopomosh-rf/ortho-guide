import json
R='/home/claude/night/lam/r/src/'; TT=json.load
TITLES={'achil':{"ru":"Шов ахиллова сухожилия","he":"תפירת גיד אכילס","ar":"خياطة وتر أخيل","en":"Achilles tendon repair"},
'dura':{"ru":"Надрыв оболочки спинного мозга при операции на позвоночнике (дуротомия)","he":"קרע בקרום חוט השדרה בניתוח בעמוד השדרה (דורוטומיה)","ar":"تمزّق غشاء الحبل الشوكي أثناء عملية العمود الفقري (بَضْع الجافية)","en":"Tear of the spinal cord membrane during spine surgery (durotomy)"}}
for top,data,tm,P in [('achil','achil_data.py','timing_achil.json','AC'),('dura','dura_data.py','timing_dura.json','DU')]:
    g={};exec(open(data).read(),g); A=json.load(open('/home/claude/ttsrepo/%s.json'%top))
    t=json.load(open(R+tm)); secs=[]
    for x in t[:-1]:
        i=x['id']; h=g['H'][i]
        secs.append({"h":{"ru":x['head'],"he":h[0],"ar":h[1],"en":h[2]},"li":[{l:A[f'{l}_{i}'] for l in ['ru','he','ar','en']}]})
    json.dump({"title":TITLES[top],"secs":secs,"src":[]},open(f'{top}_page.json','w'),ensure_ascii=False,indent=1)
    print(top,len(secs))
