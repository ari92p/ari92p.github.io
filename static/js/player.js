(function(){
var box=document.getElementById('mp');
if(!box||!window.fetch)return;
var KEY='mp-state';
var $=function(id){return document.getElementById(id)};
var audio=new Audio();audio.preload='auto';
var all=[],tracks=[],ix=0,seed=0,sh=true,lp=false,wantPlay=false,savedAt=0,fails=0;
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
function save(force){var n=Date.now();if(!force&&n-savedAt<500)return;savedAt=n;
try{localStorage.setItem(KEY,JSON.stringify({r:seed,h:sh,l:lp,i:ix,f:tracks[ix]?tracks[ix].file:'',t:audio.currentTime||0,v:audio.volume,p:wantPlay&&!audio.paused}))}catch(e){}}
function shuffle(a,x){var r=function(){x|=0;x=x+0x6D2B79F5|0;var t=Math.imul(x^x>>>15,1|x);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),k=a[i];a[i]=a[j];a[j]=k}return a}
function order(){var f=tracks[ix]?tracks[ix].file:null;tracks=sh?shuffle(all.slice(),seed):all.slice();
if(f){for(var i=0;i<tracks.length;i++){if(tracks[i].file===f){ix=i;break}}}}
function modes(){var a=$('mp-shuf'),b=$('mp-loop');a.setAttribute('aria-pressed',sh?'true':'false');b.setAttribute('aria-pressed',lp?'true':'false');
a.classList.toggle('on',sh);b.classList.toggle('on',lp);audio.loop=lp}
function playable(f){var m=/\.ogg$/i.test(f)?'audio/ogg; codecs="vorbis"':'audio/mpeg';return audio.canPlayType(m)!==''}
function src(f){return '/static/audio/'+encodeURIComponent(f)}
function fmt(t){if(!isFinite(t))return '--:--';t=Math.floor(t);return ('0'+Math.floor(t/60)).slice(-2)+':'+('0'+t%60).slice(-2)}
function clock(){$('mp-time').textContent=fmt(audio.currentTime||0)+' / '+fmt(audio.duration)}
function mark(){var f=tracks[ix]?tracks[ix].file:'',list=$('mp-list');
[].forEach.call(list.querySelectorAll('button'),function(b){var on=b.getAttribute('data-f')===f;b.classList.toggle('on',on);if(on){b.setAttribute('aria-current','true');
var top=b.offsetTop,h=b.offsetHeight;if(top<list.scrollTop)list.scrollTop=top;else if(top+h>list.scrollTop+list.clientHeight)list.scrollTop=top+h-list.clientHeight}else b.removeAttribute('aria-current')})}
function show(){$('mp-title').textContent=tracks[ix]?tracks[ix].title:'';
$('mp-play').textContent=audio.paused?'▶':'❚❚';$('mp-play').setAttribute('aria-label',audio.paused?'Play':'Pause');clock();mark()}
function tryPlay(){wantPlay=true;var p=audio.play();if(p&&p.catch)p.catch(function(){wantPlay=false;show()})}
function open(i,at,play){ix=i;audio.src=src(tracks[ix].file);
if(at){audio.addEventListener('loadedmetadata',function f(){audio.removeEventListener('loadedmetadata',f);try{audio.currentTime=at}catch(e){}})}
show();if(play)tryPlay();save(true)}
function next(d){var n=tracks.length;open((ix+d+n)%n,0,wantPlay||!audio.paused)}
var s0=load(),early=false;
audio.volume=typeof s0.v==='number'?Math.min(1,Math.max(0,s0.v)):0.6;
if(s0.f){early=true;wantPlay=!!s0.p;audio.src=src(s0.f);
if(s0.t){audio.addEventListener('loadedmetadata',function f(){audio.removeEventListener('loadedmetadata',f);try{audio.currentTime=s0.t}catch(e){}})}
if(wantPlay){var p0=audio.play();if(p0&&p0.catch)p0.catch(function(){wantPlay=false;if(tracks.length)show()})}}
fetch('/static/audio/playlist.json').then(function(r){return r.ok?r.json():[]}).then(function(d){
d.forEach(function(s){s.tracks.forEach(function(t){if(playable(t.file))all.push(t)})});
if(!all.length)return;
seed=typeof s0.r==='number'?s0.r:Math.floor(Math.random()*4294967296);
sh=s0.h!==false;lp=!!s0.l;order();
var ul=$('mp-list');
all.forEach(function(t){var li=document.createElement('li'),b=document.createElement('button');b.type='button';b.textContent=t.title;b.title=t.title;b.setAttribute('data-f',t.file);li.appendChild(b);ul.appendChild(li)});
ul.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('button');if(!b)return;var f=b.getAttribute('data-f');for(var i=0;i<tracks.length;i++){if(tracks[i].file===f){open(i,0,true);break}}});
var found=-1;if(early){for(var k=0;k<tracks.length;k++){if(tracks[k].file===s0.f){found=k;break}}}
box.hidden=false;
if(found>=0){ix=found;show()}else{if(early){audio.pause()}open(0,0,!!s0.p)}
$('mp-play').addEventListener('click',function(){if(audio.paused){tryPlay()}else{wantPlay=false;audio.pause()}});
$('mp-prev').addEventListener('click',function(){next(-1)});
$('mp-shuf').addEventListener('click',function(){sh=!sh;order();modes();show();save(true)});
$('mp-loop').addEventListener('click',function(){lp=!lp;modes();save(true)});
modes();
$('mp-tog').addEventListener('click',function(){var o=box.classList.toggle('open');this.setAttribute('aria-expanded',o?'true':'false');this.setAttribute('aria-label',o?'Hide playlist':'Show playlist');if(o)mark()});
$('mp-next').addEventListener('click',function(){next(1)});
$('mp-vol').value=Math.round(audio.volume*100);
$('mp-vol').addEventListener('input',function(){audio.volume=this.value/100;save(true)});
audio.addEventListener('play',function(){show();save(true)});
audio.addEventListener('pause',function(){show();save(true)});
audio.addEventListener('playing',function(){fails=0});
audio.addEventListener('ended',function(){next(1)});
audio.addEventListener('error',function(){if(++fails<=tracks.length&&tracks.length>1)next(1)});
audio.addEventListener('loadedmetadata',clock);
audio.addEventListener('durationchange',clock);
audio.addEventListener('timeupdate',function(){clock();save(false)});
window.addEventListener('pagehide',function(){save(true)});
}).catch(function(){});
})();
