const imagens = [
  "/img/img1.png",
  "/img/img2.png",
  "/img/img3.png",
  "/img/img4.png",
];

let imgAtual = 0;

const img = document.querySelector(".slide img");

document.getElementById("next").onclick = () =>{
    imgAtual++;
    if(imgAtual >= imagens.length){
        imgAtual = 0;
    }
    img.src = imagens[imgAtual];
};
document.getElementById("prev").onclick = () =>{
    imgAtual--;
    if(imgAtual < 0){
        imgAtual = imagens.length - 1;
    }
    img.src = imagens[imgAtual];
};

