// --- GERAR QR CODE ---
let dados = "RA: 202501234 | João da Silva | DS-1";
let qr = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(dados);

document.getElementById("qrcode-img").src = qr;

document.getElementById("download-btn").addEventListener("click", function () {

    html2canvas(document.querySelector("#card")).then(canvas => {

        let link = document.createElement("a");
        link.download = "carteirinha_senai.png";
        link.href = canvas.toDataURL("carteirinha.png");
        link.click();

    });
});

document.getElementById("nomeUsuario").textContent = sessionStorage.getItem("nome");
document.getElementById("raUsuario").textContent = sessionStorage.getItem("ra");

// function alterarDados(){
//     const novoNome = document.getElementById("nome").value;
//     const novoRa = document.getElementById("ra").value;
//     const displayNome = document.getElementById("displayNome");
//     const displayRa = document.getElementById("displayRa");

//     if (novoNome.trim() !== '' && novoRa.trim() !== ''){
//         displayNome.textContent = novoNome;
//         displayRa.textContent = novoRa;
//     }

// }