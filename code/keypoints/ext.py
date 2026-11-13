import re,html,sys
for p in sys.argv[1:]:
    s=open(f'/home/claude/ortho-guide/ops/{p}.html').read()
    m=s.find('<main>'); i=s.find('<div data-l="ru">',m); j=s.find('<div data-l="he">',i); t=s[i:j]
    t=re.sub(r'<section class="key".*?</section>','',t,flags=re.S)
    print('=====',p)
    for h,b in re.findall(r'<h2>(.*?)</h2>(.*?)</section>',t,re.S):
        h=re.sub('<[^>]+>','',h)
        if h.startswith(('Источники','Первые часы после операции','Защита от инфекции','Подготовка','Лекарства перед')): continue
        b=re.sub('<[^>]+>',' ',b); b=re.sub(r'\s+',' ',html.unescape(b)).strip()
        n=700 if re.search('срочно|Когда|скор|тревож',h,re.I) else 220
        print('##',h,'|',b[:n])
