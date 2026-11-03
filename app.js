function setL(l){document.body.className=l;var d=l=='ru'?'ltr':'rtl';document.documentElement.dir=d;document.documentElement.lang=l;
document.querySelectorAll('.lang button').forEach(function(b){b.classList.toggle('on',b.dataset.k==l)});try{localStorage.lang=l}catch(e){}
document.querySelectorAll('video').forEach(function(v){if(!v.closest('[data-l='+l+']'))v.pause()})}
function seek(l,t){var v=document.getElementById('v_'+l);v.currentTime=t;v.play();return false}
var q=(location.hash.match(/lang=(ru|he|ar)/)||[])[1];setL(q||(function(){try{return localStorage.lang}catch(e){}})()||'he');