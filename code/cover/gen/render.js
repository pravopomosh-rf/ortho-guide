const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=JSON.parse(fs.readFileSync('data.json'));for(const o of D)if(o.v=='thr3bv')o.fr=[0,0];const only=process.argv[2];
const T={ru:['Отделение ортопедии','Видео','с озвучкой и субтитрами'],he:['מחלקה אורתופדית','סרטון','עם קריינות וכתוביות'],ar:['قسم جراحة العظام','فيديو','مع تعليق صوتي ونص على الشاشة'],en:['Orthopedics Department','Video','with voice-over and captions']};
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve('tpl.html'));
for(const o of D){ if(only&&!only.split(',').includes(o.v))continue;
 const t=T[o.l];const rtl=(o.l=='he'||o.l=='ar');
 let src,cls='';
 if(o.img){src='file:///home/claude/ortho-guide/media/img/'+o.img; if(/^(lami_|ankle_anatomy|spine_disc|vcf)/.test(o.img))cls='c';if(/^(tkr_ill|thr_ill)/.test(o.img))cls='cut';}
 else {src='file://'+path.resolve('ill/'+(o.v=='thr3bv'?'stairs':o.v)+'_'+o.l+'.png');cls='fr';}
 const durTxt=rtl? `${t[1]} · <span dir="ltr">${o.dur}</span>`:`${t[1]} · ${o.dur}`;
 const h=`<div class="brand">${t[0]}</div><div class="tag">${esc(o.tag)}</div><h1>${esc(o.h1)}</h1>${o.sub?`<div class="sub">${esc(o.sub)}</div>`:''}<div class="card"><img class="${cls}" src="${src}"></div><div class="play"><div class="btn"></div><div class="dur">${durTxt}<small>${t[2]}</small></div></div>`;
 await p.evaluate(async([h,l,rtl])=>{document.body.className=l;document.documentElement.dir=rtl?"rtl":"ltr";document.body.innerHTML=h;await document.fonts.ready;await new Promise(r=>setTimeout(r,300));
  const e=document.querySelector('h1');let f=96;e.style.fontSize=f+'px';
  const fit=()=>e.scrollWidth>e.clientWidth||e.offsetHeight>f*1.4*3;
  while(fit()&&f>52){f-=2;e.style.fontSize=f+'px'}},[h,o.l,rtl]);
 await p.evaluate(()=>Promise.all([document.fonts.ready,...[...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))]));
 await p.screenshot({path:`out/${o.v}_${o.l}.png`});
}
await b.close();})();
