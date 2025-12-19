import conexao from "../infra/conexao.js";

export async function listarCadastro(req, res) {
  try {
    const [rows] = await conexao.query("SELECT 1");
    res.json({ msg: "Banco conectado", rows });
  } catch (error) {
    console.error(error);
    res.status(500).json({ erro: "Erro ao conectar ao banco." });
  }
}

export async function criarCadastro(req, res) {
  const { nome, email, senha } = req.body;
  if (!nome || !email || !senha) {
    return res.status(400).json({ erro: "Dados obrigatórios faltando!" });
  };
  try {
    const sql = `
    insert into pessoas (nome, email, senha)
    values(?, ?, ?)
    `;

    await conexao.execute(sql, [nome, email, senha]);
    res.status(201).json({ msg: "Cadastrado com sucesso!" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ erro: "Erro ao cadastrar" });
  };
};

export function atualizarCadastro(req, res) {
  const { id } = req.params; // {}garantir compatibilidade
  res.send(`Cadastro ${id} atualizado.`);
}

export function deletarCadastro(req, res) {
  const { id } = req.params;
  res.send(`Cadastro ${id} deletado.`);
}

// document.getElementById("loginForm").addEventListener("submit", (e) => {
//   e.preventDefault();
//   const nome = document.getElementById("nome").value.trim();
//   const ra = document.getElementById("ra").value.trim();

//   // validação minima

//   if (!nome || !ra) {
//     alert("Preencher todos os campos.");
//     return;
//   }
//   //guardar dados (apenas para fim didaticos)
//   sessionStorage.setItem("nome", nome);
//   sessionStorage.setItem("ra", ra);

//   window.location.href = "carteirinha.html";
// });
