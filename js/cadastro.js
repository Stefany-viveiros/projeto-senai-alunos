document.getElementById("loginForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const nome = document.getElementById("nome").value.trim();
  const ra = document.getElementById("ra").value.trim();

  // validação minima

  if (!nome || !ra) {
    alert("Preencher todos os campos.");
    return;
  }
  //guardar dados (apenas para fim didaticos)
  sessionStorage.setItem("nome", nome);
  sessionStorage.setItem("ra", ra);

  window.location.href = "carteirinha.html";
});
