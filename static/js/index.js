// diretorio das imagens dentro de um array
const imagens = [
  "/img/img1.png",
  "/img/img2.png",
  "/img/img3.png",
  "/img/img4.png",
];

let imgAtual = 0;  // contador para as imagens

const img = document.getElementById("imagem");
const next = document.querySelector(".next");
const prev = document.querySelector(".prev");

// botao para passar para a proxima imagem
next.addEventListener("click", () =>{
    imgAtual++; //ir para a proxima imagem
    if(imgAtual >= imagens.length){
        imgAtual = 0;
    }
    trocarImagem();
});

// botao para voltar para imagem anterior
prev.addEventListener("click", () =>{
    imgAtual--; //voltar para a proxima imagem
    if(imgAtual < 0){
        imgAtual = imagens.length - 1; // para deixar em loop
    }
    trocarImagem();
});

// efeito de transição de imagem
function trocarImagem(){
    img.style.opacity = 0;

    setTimeout(() =>{
        img.src = imagens[imgAtual];
        img.style.opacity = 1;
    },200);
};