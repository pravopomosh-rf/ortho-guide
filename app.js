function setL(l){document.body.className=l;var d=l=='ru'?'ltr':'rtl';document.documentElement.dir=d;document.documentElement.lang=l;
document.querySelectorAll('.lang button').forEach(function(b){b.classList.toggle('on',b.dataset.k==l)});try{localStorage.lang=l}catch(e){}
document.querySelectorAll('video').forEach(function(v){if(!v.closest('[data-l='+l+']'))v.pause()})}
function seek(l,t){var v=document.getElementById('v_'+l);v.currentTime=t;v.play();return false}
var q=(location.hash.match(/lang=(ru|he|ar)/)||[])[1];setL(q||(function(){try{return localStorage.lang}catch(e){}})()||'he');
(function(){if(!/[?&#]v=1/.test(location.search+location.hash))return;function go(){var l=document.body.className||'he',e=document.getElementById('video_'+l);if(e)e.scrollIntoView({behavior:'smooth',block:'start'})}if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',go);else go();setTimeout(go,400)})();
