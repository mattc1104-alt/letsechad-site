import re,sys,glob,html,os
try:
    from quizzes import QUIZ
except Exception:
    QUIZ={}
WM={'parshat-bereshit':'בראשית','parshat-chayei-sarah':'חיי שרה','parshat-eikev':'עקב','parshat-emor':'אמור','parshat-ki-tisa':'כי תשא','parshat-korach':'קרח','parshat-mikeitz':'מקץ','parshat-nitzavim':'נצבים','parshat-shelach':'שלח לך','parshat-tazria-metzora':'תזריע','parshat-terumah':'תרומה','parshat-vaera':'וארא','parshat-vayeshev':'וישב','parshat-vayikra':'ויקרא','parshat-yitro':'יתרו','parshat-bamidbar':'במדבר','isaiah-53-academic':'עבדי','reading-isaiah-53-honestly':'עבדי','returning-ephraim-to-the-field':'אפרים','the-king-in-the-field':'אלול','the-temple':'מקדש','worthy-is-the-lamb':'השה'}
CSS='''<style>
.pv-progress{position:fixed;top:0;left:0;right:0;height:3px;background:var(--gold);transform-origin:0 50%;transform:scaleX(0);z-index:1200}
.pv-wm{position:absolute;top:50%;right:-4%;transform:translateY(-50%);font-family:var(--serif);font-size:12rem;line-height:1;color:rgba(191,155,44,.06);direction:rtl;pointer-events:none;user-select:none;z-index:1;white-space:nowrap}
.pv-meta{font-family:var(--sans,system-ui);font-size:.68rem;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.4);margin:.9rem 0 0}
.t-body-inner>p:first-of-type::first-letter{float:left;font-size:3.4em;line-height:.82;padding:.06em .12em 0 0;color:var(--bark);font-weight:500}
.pv-quiz{background:var(--parch,#F5EDD8);border-left:4px solid var(--gold);border-radius:0 5px 5px 0;padding:1.8rem;margin:0 0 2.6rem}
.pv-quiz .pv-quiz-lead{font-family:var(--serif);font-size:1.05rem;line-height:1.7;color:#2c2313;margin:0 0 1rem}
.pv-quiz .pv-lbl{font-family:var(--sans,system-ui);font-size:.64rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#a07f16;margin:0 0 .8rem}
.pv-quiz input{position:absolute;opacity:0;pointer-events:none}
.pv-quiz label{display:block;font-family:var(--serif);font-size:1.02rem;line-height:1.5;color:#33270f;background:#FBF7EF;border:1px solid rgba(191,155,44,.4);border-radius:4px;padding:.85rem 1.1rem;margin:.55rem 0;cursor:pointer;transition:border-color .2s,background .2s}
.pv-quiz label:hover{border-color:var(--gold)}
.pv-quiz input:checked+label{border-color:var(--bark);background:rgba(62,44,20,.06)}
.pv-quiz input:checked~label.pv-correct{border-color:var(--gold);background:rgba(191,155,44,.14);box-shadow:inset 0 0 0 1px var(--gold)}
.pv-quiz .pv-quiz-reveal{display:none;margin-top:1.2rem;border-top:1px solid rgba(191,155,44,.35);padding-top:1.2rem}
.pv-quiz input:checked~.pv-quiz-reveal{display:block;animation:pvUp .5s ease both}
.pv-quiz .pv-quiz-reveal p{font-family:var(--serif);font-size:1.02rem;line-height:1.7;color:#2c2313;margin:0}
@keyframes pvUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.pv-js .pv-fx{opacity:0;transform:translateY(14px);transition:opacity .7s ease,transform .7s ease}
.pv-js .pv-fx.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.pv-js .pv-fx{opacity:1;transform:none;transition:none}.pv-quiz input:checked~.pv-quiz-reveal{animation:none}}
@media(max-width:560px){.pv-wm{font-size:6.5rem;right:-10%}.pv-quiz{padding:1.3rem}}
</style>
<script>
(function(){
document.body.classList.add('pv-js');
var b=document.createElement('div');b.className='pv-progress';document.body.appendChild(b);
function u(){var d=document.documentElement,t=d.scrollTop||document.body.scrollTop,h=d.scrollHeight-d.clientHeight;b.style.transform='scaleX('+(h>0?Math.min(1,t/h):0)+')';}
window.addEventListener('scroll',u,{passive:true});window.addEventListener('resize',u);u();
var els=document.querySelectorAll('.t-body-inner blockquote,.pull,.pv-quiz,.found-box,.bless,.s-div');
els.forEach(function(el){el.classList.add('pv-fx');});
if('IntersectionObserver' in window){
var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');o.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(el){o.observe(el);});
}else{els.forEach(function(el){el.classList.add('on');});}
})();
</script>
'''
def enhance(f):
    key=f[:-5]
    s=open(f,encoding='utf-8').read()
    if 'pv-progress' in s: return 'skip(already)'
    # watermark
    wm=WM.get(key)
    if wm:
        m=re.search(r'(<(header|section|div) class="t-hero"[^>]*>)',s)
        if m: s=s[:m.end()]+'<span class="pv-wm" aria-hidden="true">%s</span>'%wm+s[m.end():]
    # reading time after title h1
    txt=re.sub(r'<style.*?</style>','',s,flags=re.S); txt=re.sub(r'<script.*?</script>','',txt,flags=re.S); txt=re.sub(r'<[^>]+>',' ',txt)
    words=len(txt.split()); mins=max(3,round(words/220))
    m=re.search(r'(<h1 class="t-title"[^>]*>.*?</h1>)',s,re.S)
    if m: s=s[:m.end()]+'\n<p class="pv-meta">%d min read</p>'%mins+s[m.end():]
    # quiz after t-body-inner open
    q=QUIZ.get(key)
    if q:
        m=re.search(r'(<div class="t-body-inner"[^>]*>)',s)
        if m: s=s[:m.end()]+'\n'+q+'\n'+s[m.end():]
    s=s.replace('</body>',CSS+'</body>',1)
    open(f[:-5]+'-v2.html','w',encoding='utf-8').write(s)
    return 'ok wm=%s quiz=%s %dmin'%(bool(wm),bool(q),mins)
for f in sorted(glob.glob('*.html')):
    if f.endswith('-v2.html'): continue
    print(f, enhance(f))
