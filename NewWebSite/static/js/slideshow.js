document.addEventListener('DOMContentLoaded', function(){
  const slides = document.querySelectorAll('.slideshow .slide');
  if(!slides.length) return;
  let i=0;
  slides.forEach((s, idx)=>{ if(idx!==0) s.style.display='none'; });
  setInterval(()=>{
    slides[i].style.opacity=0; slides[i].style.display='none';
    i = (i+1)%slides.length;
    slides[i].style.display='block'; slides[i].style.opacity=1;
  }, 3500);
});
