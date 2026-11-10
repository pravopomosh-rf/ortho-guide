// AI Studio TTS runner (Charon). Вставлять в вкладку aistudio.google.com/u/N/generate-speech через javascript_tool.
// 1) setup: Create new dialog -> Speaker 1 -> поиск Charon -> карточка -> close
// 2) runQ(topic, keys): текст из tts-data/<topic>.json, принимать клип только если data:audio > 20 КБ и src не меняется 6 с; лог window.jobLog, ошибка квоты -> window.jobErr
// 3) mkSave(): программный клик по ссылке-blob (лучше в Playwright: page.waitForEvent('download') → saveAs в Загрузки); confirmSaved(name) — только после проверки файла
// СОХРАНЯТЬ ПОСЛЕ КАЖДЫХ 3–4 КЛИПОВ (вкладка падает от памяти). Распаковка: unpack.py -> lam/r/public/aud/<topic>/<lang>/<ID>.wav
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
window.setupCharon=async function(){
 const el=[...document.querySelectorAll('*')].find(e=>e.childElementCount===0&&e.textContent.trim()==='Create new dialog'); if(el){el.click(); await sleep(2500);}
 [...document.querySelectorAll('button')].find(b=>/^Speaker 1/.test(b.innerText.trim())).click(); await sleep(2000);
 const inp=[...document.querySelectorAll('input')].find(i=>/Search/.test(i.placeholder||''));
 Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(inp,'Charon'); inp.dispatchEvent(new Event('input',{bubbles:true})); await sleep(2000);
 [...document.querySelectorAll('button.voice-card-content')].find(b=>/Charon/.test(b.innerText)).click(); await sleep(1500);
 const cl=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()==='close'); if(cl) cl.click();
 window._aud={}; window._saved={}; window._batchN=0; window.jobLog=[]; window.jobErr='';
};
window.durOf=async function(src){const b=await fetch(src).then(r=>r.arrayBuffer()); const ab=await new OfflineAudioContext(1,1,24000).decodeAudioData(b); return ab.duration;};
window.runQ=async function(topic,keys){ window.jobDone=false;
 const d=await fetch('https://raw.githubusercontent.com/pravopomosh-rf/ortho-guide/tts-data/'+topic+'.json?t='+Date.now()).then(r=>r.json());
 for(const k of keys){ if(window._aud[topic+'/'+k]) continue;
  const ta=document.querySelector('textarea'); Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(ta,d[k]); ta.dispatchEvent(new Event('input',{bubbles:true})); await sleep(400);
  const old=(document.querySelector('audio')||{}).src||'';
  [...document.querySelectorAll('button')].find(b=>/^Run/.test(b.innerText.trim())).click();
  let last='',same=0,t0=Date.now(),err='';
  while(Date.now()-t0<240000){ await sleep(1000); const a=document.querySelector('audio'); const s=a?a.src:'';
   const ms=[...document.querySelectorAll('ms-callout,.error,[role=alert],mat-snack-bar-container')].map(e=>e.innerText).join(' ')+(/Quota limit reached/.test(document.body.innerText)?' Quota limit reached':'');
   if(/quota|exceed|limit|failed|error/i.test(ms)){err=ms.slice(0,120);break;}
   if(s&&s!==old&&s.startsWith('data:audio')&&s.length>20000){ if(s===last) same++; else {same=0;last=s;} if(same>=6) break; } }
  if(err){window.jobLog.push(k+' ERR '+err); window.jobErr=err; break;}
  if(!last){window.jobLog.push(k+' TIMEOUT'); window.jobErr='timeout'; break;}
  const du=await durOf(last); window._aud[topic+'/'+k]=last; window.jobLog.push(k+' '+du.toFixed(1)+'s cps '+(d[k].length/du).toFixed(1)); }
 window.jobDone=true; };
window.mkSave=function(acct){ window._batchN++; const keys=Object.keys(window._aud).filter(k=>!window._saved[k]); const obj={}; keys.forEach(k=>obj[k]=window._aud[k]);
 const name='tts_'+acct+'_b'+String(window._batchN).padStart(2,'0')+'.json';
 window._pending=window._pending||{}; window._pending[name]=keys;
 const b=document.createElement('a'); b.href=URL.createObjectURL(new Blob([JSON.stringify(obj)],{type:'application/json'})); b.download=name; b.className='savebtn'; b.textContent='SAVE '+name;
 b.style.cssText='position:fixed;left:0;top:0;width:10px;height:10px;opacity:0;z-index:2147483647';
 document.body.appendChild(b); b.click(); return name+' '+keys.length; };
// удалить из памяти только после проверки, что файл лёг в Загрузки
window.confirmSaved=function(name){ (window._pending[name]||[]).forEach(k=>{window._saved[k]=1; delete window._aud[k];}); delete window._pending[name]; document.querySelectorAll('a.savebtn').forEach(a=>{if(a.download===name)a.remove()}); return name+' ok'; };
