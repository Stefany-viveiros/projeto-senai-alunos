import express from "express";
import conexao from "../infra/conexao.js";

const app = express();
app.use(express.json());

app.get("/", (req, res) =>{
    res.send('Ola');
});


export default app;