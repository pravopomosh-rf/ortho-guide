(()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));
window.idbPut=(k,v)=>new Promise((res,rej)=>{const o=indexedDB.open('xfer2',1);o.onupgradeneeded=()=>o.result.createObjectStore('c');o.onsuccess=()=>{const tx=o.result.transaction('c','readwrite');tx.objectStore('c').put(v,k);tx.oncomplete=()=>{o.result.close();res()};tx.onerror=rej}});
window.idbKeys=()=>new Promise(res=>{const o=indexedDB.open('xfer2',1);o.onupgradeneeded=()=>o.result.createObjectStore('c');o.onsuccess=()=>{const r=o.result.transaction('c').objectStore('c').getAllKeys();r.onsuccess=()=>{o.result.close();res(r.result)}}});
function split(t,lim){if(t.length<=lim)return[t];const s=t.match(/[^.!?؟。]+[.!?؟]+["»”)]*\s*|[^.!?؟]+$/g)||[t];const out=[];let cur='';for(const x of s){if((cur+x).length>lim&&cur){out.push(cur.trim());cur=''}cur+=x}if(cur.trim())out.push(cur.trim());return out}
window.loadQ=async keys=>{const R='https://raw.githubusercontent.com/pravopomosh-rf/ortho-guide/tts-data/manus/';const a=await fetch(R+'todo.json?t='+Date.now()).then(r=>r.json());const b=await fetch(R+'todo_priority.json?t='+Date.now()).then(r=>r.json());const T={...a,...b};const Q=[];for(const k of keys){const t=T[k];if(!t){continue}const lang=k.split('_')[1];const p=split(t,(lang=='he'||lang=='ar')?300:380);if(p.length==1)Q.push([k,p[0]]);else p.forEach((x,i)=>Q.push([k+'|'+(i+1)+'of'+p.length,x]))}window.Q=Q;return Q.length};
window.runQ=async()=>{window.jobLog=window.jobLog||[];window.jobErr='';window.jobDone=false;const have=new Set(await idbKeys());
 for(const [k,t] of window.Q){if(have.has(k))continue;
  const ta=document.querySelector('textarea[aria-label="Speech block text"]')||document.querySelector('textarea');
  Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(ta,t);ta.dispatchEvent(new Event('input',{bubbles:true}));await sleep(600);
  const old=(document.querySelector('audio')||{}).src||'';
  const rb=[...document.querySelectorAll('button')].find(b=>/^Run/.test(b.innerText.trim()));rb.click();
  let last='',same=0,t0=Date.now(),err='';
  while(Date.now()-t0<180000){await sleep(2000);const a=document.querySelector('audio');const s=a?a.src:'';
   const ms=[...document.querySelectorAll('ms-callout,.error,[role=alert],mat-snack-bar-container,.mat-mdc-snack-bar-label')].map(e=>e.innerText).join(' ');
   if(/quota|exceed|limit|failed|error|permission/i.test(ms)){err=ms.slice(0,140);break}
   const running=[...document.querySelectorAll('button')].some(b=>/^Stop/.test(b.innerText.trim()));if(s&&s!==old&&(s.length>20000||s.startsWith('blob:'))&&!running){if(s===last)same++;else{same=0;last=s}if(same>=2)break}}
  if(err){window.jobLog.push(k+' ERR '+err);window.jobErr=err;break}
  if(!last){window.jobLog.push(k+' TIMEOUT');window.jobErr='timeout';break}
  let v=last;if(v.startsWith('blob:')){const bl=await fetch(v).then(r=>r.blob());v=await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(bl)})}
  await idbPut(k,v);window.jobLog.push(k+' ok '+Math.round(v.length/1000)+'k')}
 window.jobDone=true};
return 'ok'})()
