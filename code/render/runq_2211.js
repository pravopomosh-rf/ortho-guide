// Раннер AI Studio 22.11 (u/N/generate-speech). Подготовка вкладки руками: Create new dialog → (подождать 3 с) Speaker 1 → поиск Charon → карточка → close → Style «calm, slow, warm and confident» Enter → Esc.
// Вставить весь блок ниже через javascript_tool, затем: await loadQ([...ключи todo]); window.Q.length=Math.min(25,Q.length); runQ();  опрос: window.jobLog / jobErr / jobDone.
// Клипы → IDB 'xfer2' store 'c' (общий для всех u/N). Скачивание: вкладка aistudio.google.com/robots.txt, вставить mk/del (внизу), await mk('tts_u_ДДММ_bN.json') → клик курсором по экрану → stage → merge_parts.py → proc_tts.py → await del().
// Блоки ответа: audio.src = data:audio/wav (готов, когда кнопки Stop нет и src не меняется 4 с). u/4 — 403. Квота ≈25–27 запросов (части текста считаются отдельно).
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
   if(s&&s!==old&&s.length>20000){if(s===last)same++;else{same=0;last=s}if(same>=3)break}}
  if(err){window.jobLog.push(k+' ERR '+err);window.jobErr=err;break}
  if(!last){window.jobLog.push(k+' TIMEOUT');window.jobErr='timeout';break}
  let v=last;if(v.startsWith('blob:')){const bl=await fetch(v).then(r=>r.blob());v=await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(bl)})}
  await idbPut(k,v);window.jobLog.push(k+' ok '+Math.round(v.length/1000)+'k')}
 window.jobDone=true};
return 'ok'})()
// В runQ заменить условие готовности на: (s.length>20000||s.startsWith('blob:'))&&!running, где running = есть кнопка /^Stop/; same>=2.
// --- для вкладки robots.txt ---
// window.mk=async(name)=>{const db=await new Promise(r=>{const o=indexedDB.open('xfer2',1);o.onsuccess=()=>r(o.result)});const keys=(await new Promise(r=>{const q=db.transaction('c').objectStore('c').getAllKeys();q.onsuccess=()=>r(q.result)})).slice(0,30);const obj={};for(const k of keys){obj[k]=await new Promise(r=>{const q=db.transaction('c').objectStore('c').get(k);q.onsuccess=()=>r(q.result)})}db.close();window.dlk=keys;document.querySelectorAll('a.sv').forEach(x=>x.remove());const a=document.createElement('a');a.className='sv';a.href=URL.createObjectURL(new Blob([JSON.stringify(obj)],{type:'application/json'}));a.download=name;a.textContent='SAVE '+name;a.style.cssText='position:fixed;inset:0;display:block;font-size:40px;background:#eef;z-index:99999';document.body.appendChild(a);return keys.join(' ')};
// window.del=async()=>{const db=await new Promise(r=>{const o=indexedDB.open('xfer2',1);o.onsuccess=()=>r(o.result)});const tx=db.transaction('c','readwrite');for(const k of window.dlk)tx.objectStore('c').delete(k);await new Promise(r=>tx.oncomplete=r);db.close();return window.dlk.length};
