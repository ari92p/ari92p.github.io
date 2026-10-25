(function(){
var box=document.getElementById('mp');
if(!box||!window.fetch)return;
var KEY='mp-state';
var $=function(id){return document.getElementById(id)};
var audio=new Audio();audio.preload='none';
var lists=[],st=0,ix=0,wantPlay=false,savedAt=0;
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
function save(force){var n=Date.now();if(!force&&n-savedAt<1000)return;savedAt=n;
try{localStorage.setItem(KEY,JSON.stringify({s:st,i:ix,t:audio.currentTime||0,v:audio.volume,p:wantPlay&&!audio.paused}))}catch(e){}}
function playable(t){var m=/\.ogg$/i.test(t.file)?'audio/ogg; codecs="vorbis"':'audio/mpeg';return audio.canPlayType(m)!==''}
function track(){return lists[st].tracks[ix]}
function show(){var t=track();$('mp-title').textContent=t.title;$('mp-title').setAttribute('data-long',t.title.length>11?'1':'0');
$('mp-play').textContent=audio.paused?'▶':'❚❚';$('mp-play').setAttribute('aria-label',audio.paused?'Play':'Pause')}
function open(i,at,play){ix=i;audio.src='/static/audio/'+encodeURIComponent(track().file);
if(at){audio.addEventListener('loadedmetadata',function f(){audio.removeEventListener('loadedmetadata',f);try{audio.currentTime=at}catch(e){}})}
show();if(play){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){wantPlay=false;show()})}save(true)}
function next(d){var n=lists[st].tracks.length;open((ix+d+n)%n,0,wantPlay||!audio.paused)}
fetch('/static/audio/playlist.json').then(function(r){return r.ok?r.json():[]}).then(function(d){
lists=d.map(function(s){return {name:s.name,tracks:s.tracks.filter(playable)}}).filter(function(s){return s.tracks.length});
if(!lists.length)return;
var sel=$('mp-station');lists.forEach(function(s,i){var o=document.createElement('option');o.value=i;o.textContent=s.name;sel.appendChild(o)});
var s=load();st=(s.s>=0&&s.s<lists.length)?s.s:0;sel.value=st;
audio.volume=typeof s.v==='number'?Math.min(1,Math.max(0,s.v)):0.6;$('mp-vol').value=Math.round(audio.volume*100);
ix=(s.i>=0&&s.i<lists[st].tracks.length)?s.i:0;
box.hidden=false;open(ix,s.t||0,!!s.p);
sel.addEventListener('change',function(){st=parseInt(sel.value,10);open(0,0,wantPlay||!audio.paused)});
$('mp-play').addEventListener('click',function(){if(audio.paused){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){})}else{wantPlay=false;audio.pause()}});
$('mp-prev').addEventListener('click',function(){next(-1)});
$('mp-next').addEventListener('click',function(){next(1)});
$('mp-vol').addEventListener('input',function(){audio.volume=this.value/100;save(true)});
audio.addEventListener('play',function(){show();save(true)});
audio.addEventListener('pause',function(){show();save(true)});
audio.addEventListener('ended',function(){next(1)});
audio.addEventListener('error',function(){if(audio.src&&lists[st].tracks.length>1)next(1)});
audio.addEventListener('timeupdate',function(){save(false)});
window.addEventListener('pagehide',function(){save(true)});
}).catch(function(){});
})();
