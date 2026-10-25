/* Page changes without a reload, so the music player keeps playing between pages. */
(function(){
if(!window.fetch||!window.DOMParser||!history.pushState)return;
var cur=location.pathname,token=0;
function internal(a){
if(!a||!a.href||a.origin!==location.origin)return false;
if(a.target&&a.target!=='_self')return false;
if(a.hasAttribute('download')||a.hasAttribute('data-copy')||a.hasAttribute('data-layout'))return false;
if(/^\/static\//.test(a.pathname)||/\.(pdf|zip|png|jpe?g|gif|webp|svg|mp3|ogg|xml|json|txt)$/i.test(a.pathname))return false;
if(a.pathname===location.pathname&&a.hash)return false;
return true}
function fail(url){location.href=url}
function swap(html){
var doc=new DOMParser().parseFromString(html,'text/html');
var mp=document.getElementById('mp'),nmp=doc.getElementById('mp');
if(mp&&nmp)nmp.parentNode.replaceChild(mp,nmp);
[].forEach.call(doc.querySelectorAll('script'),function(s){s.remove()});
document.title=doc.title;
['meta[name="description"]','meta[property="og:title"]','meta[property="og:description"]','meta[property="og:url"]'].forEach(function(sel){
var o=document.head.querySelector(sel),n=doc.head.querySelector(sel);if(o&&n)o.setAttribute('content',n.getAttribute('content'))});
while(document.body.firstChild)document.body.removeChild(document.body.firstChild);
while(doc.body.firstChild)document.body.appendChild(document.adoptNode(doc.body.firstChild));
}
function go(url,push){
var my=++token;
fetch(url,{credentials:'same-origin'}).then(function(r){
if(my!==token)return null;
if(!r.ok||(r.headers.get('content-type')||'').indexOf('text/html')<0){fail(url);return null}
return r.text()}).then(function(html){
if(html===null||my!==token)return;
var u=new URL(url,location.href);
if(push)history.pushState(null,'',u.pathname+u.search+u.hash);
swap(html);
cur=location.pathname;
if(location.hash){var t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t)t.scrollIntoView();else window.scrollTo(0,0)}else window.scrollTo(0,0);
if(window.siteInit)window.siteInit();
}).catch(function(){fail(url)})}
document.addEventListener('click',function(e){
if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
var a=e.target.closest&&e.target.closest('a');
if(!internal(a))return;
e.preventDefault();go(a.href,true)});
window.addEventListener('popstate',function(){if(location.pathname!==cur)go(location.href,false)});
if('scrollRestoration' in history)history.scrollRestoration='manual';
})();
