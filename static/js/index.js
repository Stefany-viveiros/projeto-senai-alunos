// ================= CARROSSEL =================

// Seleciona os elementos
const track = document.querySelector(".carousel-track");
const slides = document.querySelectorAll(".carousel-item");
const prevBtn = document.querySelector(".carousel-btn.prev");
const nextBtn = document.querySelector(".carousel-btn.next");

let index = 0;

// Atualiza a posição do carrossel
function updateCarousel() {
    track.style.transform = `translateX(-${index * 100}%)`;
}

// Botão próximo
nextBtn.addEventListener("click", () => {
    index++;
    if (index >= slides.length) {
        index = 0;
    }
    updateCarousel();
});

// Botão anterior
prevBtn.addEventListener("click", () => {
    index--;
    if (index < 0) {
        index = slides.length - 1;
    }
    updateCarousel();
});

// Auto-play (opcional)
setInterval(() => {
    index++;
    if (index >= slides.length) {
        index = 0;
    }
    updateCarousel();
}, 5000); // troca a cada 5 segundos
