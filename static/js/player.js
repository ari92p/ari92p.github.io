(function(){
var box=document.getElementById('mp');
if(!box||!window.fetch)return;
var KEY='mp-state';
var $=function(id){return document.getElementById(id)};
var audio=new Audio();audio.preload='none';
var tracks=[],ix=0,wantPlay=false,savedAt=0;
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
function save(force){var n=Date.now();if(!force&&n-savedAt<1000)return;savedAt=n;
try{localStorage.setItem(KEY,JSON.stringify({i:ix,t:audio.currentTime||0,v:audio.volume,p:wantPlay&&!audio.paused}))}catch(e){}}
function playable(f){var m=/\.ogg$/i.test(f)?'audio/ogg; codecs="vorbis"':'audio/mpeg';return audio.canPlayType(m)!==''}
function clock(){var t=Math.floor(audio.currentTime||0);$('mp-time').textContent=('0'+Math.floor(t/60)).slice(-2)+':'+('0'+t%60).slice(-2)}
function show(){$('mp-play').textContent=audio.paused?'▶':'❚❚';$('mp-play').setAttribute('aria-label',audio.paused?'Play':'Pause');clock()}
function open(i,at,play){ix=i;audio.src='/static/audio/'+encodeURIComponent(tracks[ix]);
if(at){audio.addEventListener('loadedmetadata',function f(){audio.removeEventListener('loadedmetadata',f);try{audio.currentTime=at}catch(e){}})}
show();if(play){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){wantPlay=false;show()})}save(true)}
function next(d){var n=tracks.length;open((ix+d+n)%n,0,wantPlay||!audio.paused)}
fetch('/static/audio/playlist.json').then(function(r){return r.ok?r.json():[]}).then(function(d){
d.forEach(function(s){s.tracks.forEach(function(t){if(playable(t.file))tracks.push(t.file)})});
if(!tracks.length)return;
var s=load();
audio.volume=typeof s.v==='number'?Math.min(1,Math.max(0,s.v)):0.6;$('mp-vol').value=Math.round(audio.volume*100);
var first=(s.i>=0&&s.i<tracks.length);
box.hidden=false;open(first?s.i:Math.floor(Math.random()*tracks.length),first?(s.t||0):0,!!s.p);
$('mp-play').addEventListener('click',function(){if(audio.paused){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){})}else{wantPlay=false;audio.pause()}});
$('mp-prev').addEventListener('click',function(){next(-1)});
$('mp-next').addEventListener('click',function(){next(1)});
$('mp-vol').addEventListener('input',function(){audio.volume=this.value/100;save(true)});
audio.addEventListener('play',function(){show();save(true)});
audio.addEventListener('pause',function(){show();save(true)});
audio.addEventListener('ended',function(){next(1)});
audio.addEventListener('error',function(){if(audio.src&&tracks.length>1)next(1)});
audio.addEventListener('timeupdate',function(){clock();save(false)});
window.addEventListener('pagehide',function(){save(true)});
}).catch(function(){});
})();
