const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
for(const [f,n] of [['index.html','idx'],['ops/hip-path.html','hip'],['ops/thr.html','thr_fb']]){
await p.goto('file:///home/claude/ortho-guide/'+f+'#lang=am');await p.waitForTimeout(1200);
await p.screenshot({path:'/home/claude/amw/'+n+'.png',fullPage:false});
console.log(f, await p.evaluate(()=>document.body.className+' dir='+document.documentElement.dir+' fbnote='+!!document.querySelector('.amnote')));}
console.log('errors',errs);await b.close();})();
