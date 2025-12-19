import app from "./js/app.js";

const PORT = 3000;

//executar a porta 3000
app.listen(PORT, ()=>{
    console.log(`Servidor rodando no endereço http://localhost:${PORT}`);
});