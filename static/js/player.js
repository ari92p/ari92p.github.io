(function(){
var box=document.getElementById('mp');
if(!box||!window.fetch)return;
var KEY='mp-state';
var $=function(id){return document.getElementById(id)};
var audio=new Audio();audio.preload='none';
var tracks=[],ix=0,seed=0,wantPlay=false,savedAt=0;
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
function save(force){var n=Date.now();if(!force&&n-savedAt<1000)return;savedAt=n;
try{localStorage.setItem(KEY,JSON.stringify({r:seed,i:ix,t:audio.currentTime||0,v:audio.volume,p:wantPlay&&!audio.paused}))}catch(e){}}
function shuffle(a,x){var r=function(){x|=0;x=x+0x6D2B79F5|0;var t=Math.imul(x^x>>>15,1|x);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),k=a[i];a[i]=a[j];a[j]=k}return a}
function playable(f){var m=/\.ogg$/i.test(f)?'audio/ogg; codecs="vorbis"':'audio/mpeg';return audio.canPlayType(m)!==''}
function show(){$('mp-title').textContent=tracks[ix].title;$('mp-play').textContent=audio.paused?'▶':'❚❚';$('mp-play').setAttribute('aria-label',audio.paused?'Play':'Pause')}
function open(i,at,play){ix=i;audio.src='/static/audio/'+encodeURIComponent(tracks[ix].file);
if(at){audio.addEventListener('loadedmetadata',function f(){audio.removeEventListener('loadedmetadata',f);try{audio.currentTime=at}catch(e){}})}
show();if(play){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){wantPlay=false;show()})}save(true)}
function next(d){var n=tracks.length;open((ix+d+n)%n,0,wantPlay||!audio.paused)}
fetch('/static/audio/playlist.json').then(function(r){return r.ok?r.json():[]}).then(function(d){
d.forEach(function(s){s.tracks.forEach(function(t){if(playable(t.file))tracks.push(t)})});
if(!tracks.length)return;
var s=load();
audio.volume=typeof s.v==='number'?Math.min(1,Math.max(0,s.v)):0.6;$('mp-vol').value=Math.round(audio.volume*100);
seed=typeof s.r==='number'?s.r:Math.floor(Math.random()*4294967296);
tracks=shuffle(tracks,seed);
var first=(s.i>=0&&s.i<tracks.length);
box.hidden=false;open(first?s.i:0,first?(s.t||0):0,!!s.p);
$('mp-play').addEventListener('click',function(){if(audio.paused){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){})}else{wantPlay=false;audio.pause()}});
$('mp-prev').addEventListener('click',function(){next(-1)});
$('mp-next').addEventListener('click',function(){next(1)});
$('mp-vol').addEventListener('input',function(){audio.volume=this.value/100;save(true)});
audio.addEventListener('play',function(){show();save(true)});
audio.addEventListener('pause',function(){show();save(true)});
audio.addEventListener('ended',function(){next(1)});
audio.addEventListener('error',function(){if(audio.src&&tracks.length>1)next(1)});
audio.addEventListener('timeupdate',function(){save(false)});
window.addEventListener('pagehide',function(){save(true)});
}).catch(function(){});
})();
