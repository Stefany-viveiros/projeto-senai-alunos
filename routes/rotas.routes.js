import {Router} from "express";
const router = Router();
//rota para teste
router.get('/', (req,res) =>{
    res.send('API rodando');
});


//rota para cadastro
router.post('/cadastro', (req,res)=>{
    res.send('Cadastrado com sucesso.');
});

// lista de cadastro
router.get('/cadastro', (req, res) =>{
    res.send('Lista de cadastro.');
});

// atualizar cadastro
router.put('/cadastro/:id', (req, res) =>{
    res.send(`Cadastro ${req.params.id} atualizado.`);
});

// deletar cadastro
router.delete('/cadastro/:id', (req, res) =>{
    res.send(`Cadastro ${req.params.id} deletado.`);
});
export default router;

// usa export quando se usa import
// req.params é usado para identificar o recurso pela rota
// req.body contem os dados enviados na requisição