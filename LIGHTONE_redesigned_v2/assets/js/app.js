const pages=[...document.querySelectorAll('.page')];
const navLinks=[...document.querySelectorAll('.site-nav a')];
const nav=document.querySelector('.site-nav');
const toggle=document.querySelector('.nav-toggle');
function showPage(){
  const id=(location.hash||'#home').replace('#','');
  const target=document.getElementById(id)||document.getElementById('home');
  pages.forEach(page=>page.classList.toggle('active',page===target));
  navLinks.forEach(link=>{
    const current=link.getAttribute('href')===`#${target.id}`;
    if(current) link.setAttribute('aria-current','page'); else link.removeAttribute('aria-current');
  });
  document.title=`LIGHT ONE | ${target.id.replaceAll('-',' ')}`;
  if(document.activeElement?.classList?.contains('site-nav')) return;
  target.focus({preventScroll:true});
  window.scrollTo({top:0,behavior:'smooth'});
  nav?.classList.remove('open');
  toggle?.setAttribute('aria-expanded','false');
}
toggle?.addEventListener('click',()=>{
  const open=nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded',String(open));
  toggle.setAttribute('aria-label',open?'메뉴 닫기':'메뉴 열기');
});
window.addEventListener('hashchange',showPage);
window.addEventListener('DOMContentLoaded',showPage);
