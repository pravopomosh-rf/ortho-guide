import json,re
f=open('/home/claude/ttsrepo/topics/shoulder_replacement_gpt_1111.txt').read().split('\n')
def block(a,b): return f[a-1:b]
RNG={'ru':(93,180),'he':(354,465),'ar':(468,579),'en':(582,700)}
H={'he':["מהי החלפת מפרק הכתף","החלפת כתף אנטומית או הפוכה","הכנה לניתוח ומהלך הניתוח","הימים הראשונים במחלקה","פיזיותרפיה והגבלות תנועה","שינה, לבוש, רחצה וטיפול בפצע בבית","לפני השחרור ודאו שאתם יודעים","מתי לפנות בדחיפות לעזרה רפואית"],
'ar':["ما هو استبدال مفصل الكتف","المفصل التشريحي أم المفصل العكسي","التحضير للعملية وكيف تُجرى","الأيام الأولى في القسم","العلاج الطبيعي وقيود الحركة",None,"قبل الخروج تأكدوا من أنكم تعرفون","متى يجب طلب المساعدة الطبية بشكل عاجل"],
'en':["What is shoulder replacement?","Anatomical or reverse shoulder replacement?","Preparing for surgery and the operation","Your first days on the ward","Physiotherapy and movement restrictions","Sleeping, dressing, showering, and wound care at home","Before discharge, make sure you know","When to seek urgent medical help"]}
SUB={'ru':["Анатомический","Реверсивный"],'he':["החלפת כתף אנטומית","החלפת כתף הפוכה"],'ar':["استبدال مفصل الكتف التشريحي","استبدال مفصل الكتف العكسي"],'en':["Anatomical shoulder replacement","Reverse shoulder replacement"]}
DROP=re.compile(r'^(AAOS|\+\d|pubmed|NICE|pmc\.|Индивидуальные указания|ההנחיות האישיות|تعليمات الطبيب المعالج الخاصة|Your doctor.s individual|Если инструкция непонятна$)')
secs={l:[] for l in RNG}
for l,(a,b) in RNG.items():
    lines=[x.strip() for x in block(a,b) if x.strip()]
    if l!='ru': lines=lines[0:]
    cur=None; sub=None
    for x in lines:
        if x.startswith('Последний ответ') or x.startswith('ChatGPT может'): break
        if DROP.match(x): continue
        ish = (l=='ru' and re.match(r'^\d\. ',x)) or (l!='ru' and x in [h for h in H[l] if h]) or (l=='ar' and x.startswith('النوم والملابس'))
        if ish:
            cur={'h':re.sub(r'^\d\. ','',x),'li':[]}; secs[l].append(cur); sub=None; continue
        if cur is None: continue
        if x in SUB[l]: sub=x; continue
        cur['li'].append(('<b>'+sub+'.</b> '+x) if sub else x); sub=None if not sub else sub
        if sub: sub=None
for l in secs: print(l,len(secs[l]),[len(s['li']) for s in secs[l]])
title={'ru':'Эндопротезирование плечевого сустава: анатомическое и реверсивное','he':'החלפת מפרק הכתף: אנטומית והפוכה','ar':'استبدال مفصل الكتف: التشريحي والعكسي','en':'Shoulder replacement: anatomical and reverse'}
out={'title':title,'secs':[],'src':[
 {'t':'AAOS OrthoInfo — Shoulder Joint Replacement','url':'https://orthoinfo.aaos.org/en/treatment/shoulder-joint-replacement/'},
 {'t':'AAOS OrthoInfo — Reverse Total Shoulder Replacement','url':'https://orthoinfo.aaos.org/en/treatment/reverse-total-shoulder-replacement/'},
 {'t':'Kennedy JS et al. ASSET consensus: rehabilitation after anatomic total shoulder arthroplasty. J Shoulder Elbow Surg 2020','url':'https://pubmed.ncbi.nlm.nih.gov/32534209/'},
 {'t':'NHS — Dislocated shoulder','url':'https://www.nhs.uk/conditions/dislocated-shoulder/'}]}
for i in range(8):
    n=max(len(secs[l][i]['li']) for l in secs)
    out['secs'].append({'h':{l:secs[l][i]['h'] for l in secs},'li':[{**{l:(secs[l][i]['li'][j] if j<len(secs[l][i]['li']) else '') for l in secs},'html':True} for j in range(n)]})
json.dump(out,open('/home/claude/gen/shrepl_page.json','w'),ensure_ascii=False,indent=1)
