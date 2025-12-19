import { Router } from "express"; //uso de {} para garantir compatibilidade
import {
  listarCadastro,
  criarCadastro,
  atualizarCadastro,
  deletarCadastro,
} from "../controller/cadastro.js";

const router = Router();
//rota para teste
router.get("/", (req, res) => {
  res.send("API rodando");
});

// lista de cadastro
router.get("/cadastro", listarCadastro);

// criar cadastro
router.post("/cadastro", criarCadastro);

// atualizar cadastro
router.put("/cadastro/:id", atualizarCadastro);

// deletar cadastro
router.delete("/cadastro/:id", deletarCadastro);

export default router;

// usa export quando se usa import
// req.params é usado para identificar o recurso pela rota
// req.body contem os dados enviados na requisição
