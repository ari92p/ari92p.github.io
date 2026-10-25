(function(){
var tabHandler=null,postsRender=null;
function init(){
tabHandler=null;postsRender=null;
var tabs=document.querySelectorAll('.tabs a');
if(tabs.length){
function show(){var first=tabs[0].getAttribute('data-tab');var id=(location.hash||'#'+first).slice(1);if(!document.getElementById('p-'+id))id=first;
tabs.forEach(function(a){a.classList.toggle('on',a.getAttribute('data-tab')===id)});
document.querySelectorAll('.tp').forEach(function(p){p.classList.toggle('on',p.id==='p-'+id)});}
tabHandler=show;show();}
var v=document.getElementById('visits');
if(v){try{var n=parseInt(localStorage.getItem('visits')||'0',10);
if(!sessionStorage.getItem('counted')){n+=1;localStorage.setItem('visits',String(n));sessionStorage.setItem('counted','1')}
v.textContent=String(Math.max(1,n));}catch(e){}}
var ls=document.querySelectorAll('a[data-layout]');
ls.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var v=a.getAttribute('data-layout');document.documentElement.setAttribute('data-layout',v);try{localStorage.setItem('layout',v)}catch(x){}})});
document.querySelectorAll('a[data-copy]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var txt=a.getAttribute('data-copy'),old=a.textContent;
function done(){a.textContent='copied';a.classList.add('copied');setTimeout(function(){a.textContent=old;a.classList.remove('copied')},1300)}
function fallback(){var t=document.createElement('textarea');t.value=txt;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(x){}document.body.removeChild(t);done()}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,fallback)}else{fallback()}})});
document.querySelectorAll('a[data-top]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();window.scrollTo({top:0,behavior:window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})});
var box=document.getElementById('posts');
if(box){
var per=parseInt(box.getAttribute('data-per')||'5',10);
var posts=[].slice.call(box.querySelectorAll('.post'));
posts.sort(function(a,b){return b.getAttribute('data-ts')-a.getAttribute('data-ts')});
var sortbar=document.getElementById('sortbar'),pager=document.getElementById('pager'),pagerTop=document.getElementById('pager-top');
function read(){var p=new URLSearchParams(location.hash.replace(/^#/,''));var pg=parseInt(p.get('page')||'1',10);return {page:pg>0?pg:1,old:p.get('sort')==='old'}}
function href(pg,old){var p=new URLSearchParams();if(pg>1)p.set('page',String(pg));if(old)p.set('sort','old');var h=p.toString();return h?'#'+h:'#'}
function render(){var s=read();var list=s.old?posts.slice().reverse():posts;var pages=Math.max(1,Math.ceil(list.length/per));var pg=Math.min(s.page,pages);
list.forEach(function(el,i){box.appendChild(el);el.style.display=(i>=(pg-1)*per&&i<pg*per)?'block':'none'});
sortbar.innerHTML='Sort: '+(s.old?'<a href="'+href(1,false)+'">newest first</a> | <b>oldest first</b>':'<b>newest first</b> | <a href="'+href(1,true)+'">oldest first</a>');
if(pages<2){pager.innerHTML='';}else{var h='';h+=pg>1?'<a href="'+href(pg-1,s.old)+'">&laquo; newer</a>':'<span class="off">&laquo; newer</span>';
for(var n=1;n<=pages;n++){h+=n===pg?'<b>'+n+'</b>':'<a href="'+href(n,s.old)+'">'+n+'</a>'}
h+=pg<pages?'<a href="'+href(pg+1,s.old)+'">older &raquo;</a>':'<span class="off">older &raquo;</span>';
if(s.old){h=h.replace('&laquo; newer','&laquo; earlier').replace('older &raquo;','later &raquo;')}
pager.innerHTML=h}
pagerTop.innerHTML=pager.innerHTML}
[sortbar,pager,pagerTop].forEach(function(el){el.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;e.preventDefault();var y=window.pageYOffset;var h=a.getAttribute('href');history.pushState(null,'',h==='#'?location.pathname+location.search:h);render();window.scrollTo(0,y)})});
postsRender=render;render();
}
}
window.addEventListener('hashchange',function(){if(tabHandler)tabHandler();if(postsRender)postsRender()});
window.addEventListener('popstate',function(){if(postsRender)postsRender()});
/* iPhone: after a pull-down refresh the page can come back scrolled up a little, under the clock. Reset that,
   but never fight the reader once they scroll themselves. */
var touched=false;['touchstart','wheel','keydown','mousedown'].forEach(function(ev){window.addEventListener(ev,function(){touched=true},{passive:true,capture:true})});
function fixTop(){if(touched||location.hash)return;var y=window.pageYOffset||0;if(y>0&&y<=120)window.scrollTo(0,0)}
window.addEventListener('pageshow',function(){touched=false;fixTop();setTimeout(fixTop,150);setTimeout(fixTop,500)});
window.addEventListener('load',function(){fixTop();setTimeout(fixTop,300)});
window.siteInit=init;
init();
})();
