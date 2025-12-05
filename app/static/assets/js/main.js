
const sidebar=document.getElementById('sidebar');
const overlay=document.getElementById('overlay');
const menuToggle=document.getElementById('menuToggle');

menuToggle.onclick=()=>{
  if(sidebar.classList.contains('open')){
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
  } else {
    sidebar.classList.add('open');
    overlay.classList.add('show');
  }
};

overlay.onclick=()=>{
  sidebar.classList.remove('open');
  overlay.classList.remove('show');
};