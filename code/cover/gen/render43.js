const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=JSON.parse(fs.readFileSync('data.json'));const only=process.argv[2];
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:960,height:720}});
await p.goto('file://'+path.resolve('tpl43.html'));
for(const o of D){ if(only&&!only.split(',').includes(o.v))continue;
 const rtl=(o.l=='he'||o.l=='ar');let src,cls='';
 if(o.img){src='file:///home/claude/ortho-guide/media/img/'+o.img; if(/^(lami_|ankle_anatomy|spine_disc|vcf)/.test(o.img))cls='c';if(/^(tkr_ill|thr_ill)/.test(o.img))cls='cut';}
 else {src='file://'+path.resolve('ill/'+(o.v=='thr3bv'?'stairs':o.v)+'_'+o.l+'.png');cls='fr';}
 const h=`<div class="card"><img class="${cls}" src="${src}"></div><div class="play"><div class="btn"></div><div class="dur"><span dir="ltr">${o.dur}</span></div></div>`;
 await p.evaluate(([h,l,rtl])=>{document.body.className=l;document.documentElement.dir=rtl?'rtl':'ltr';document.body.innerHTML=h},[h,o.l,rtl]);
 await p.evaluate(()=>Promise.all([document.fonts.ready,...[...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))]));
 await p.screenshot({path:`t/${o.v}_${o.l}.png`});
}
await b.close();})();
