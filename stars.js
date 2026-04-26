document.querySelectorAll(".star").forEach(star=>{
  star.onclick=()=>{
    document.getElementById("rating").value=star.dataset.value;
    document.querySelectorAll(".star").forEach(s=>s.classList.remove("selected"));
    for(let i=1;i<=star.dataset.value;i++)
      document.querySelector(`[data-value="${i}"]`).classList.add("selected");
  }
});

