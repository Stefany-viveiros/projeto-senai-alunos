# Projeto SENAI Alunos

**Sistema web de carteirinha digital para alunos**

Acesse o projeto: https://projeto-senai-alunos.onrender.com

## Sobre o projeto

O **Projeto SENAI Alunos** é uma aplicação web desenvolvida durante a formação em Programação Full Stack, com o objetivo de simular um sistema real de gerenciamento e identificação de alunos.

A aplicação permite que o aluno realize seu cadastro, faça login e tenha acesso a uma carteirinha digital contendo suas principais informações acadêmicas e um QR Code gerado individualmente.

O projeto foi desenvolvido com uma arquitetura que integra frontend, backend e banco de dados, permitindo praticar conceitos fundamentais do desenvolvimento Full Stack.

## Objetivo

O objetivo do sistema é digitalizar o processo de identificação do aluno, substituindo uma carteirinha física por uma versão acessível pela aplicação web.

Além da apresentação das informações acadêmicas, o sistema trabalha com autenticação e armazenamento estruturado dos dados dos alunos.

## Funcionalidades

### Cadastro de alunos

O sistema permite realizar o cadastro de novos alunos com informações como:

* Nome;
* Usuário;
* Registro Acadêmico (RA);
* Telefone;
* Curso;
* Turma;
* Foto;
* Senha.

Durante o cadastro, o sistema realiza validações básicas, verifica se o usuário já está registrado, valida a confirmação da senha e verifica o formato do arquivo de imagem enviado.

### Autenticação

O sistema possui fluxo de login e logout.

As senhas não são armazenadas diretamente no banco de dados. A aplicação utiliza `generate_password_hash` para gerar o hash da senha e `check_password_hash` para realizar a validação durante o login.

Após a autenticação, os dados da sessão são utilizados para controlar o acesso às funcionalidades protegidas da aplicação.

### Carteirinha digital

Após realizar o login, o aluno pode acessar sua carteirinha digital.

A carteirinha apresenta os dados cadastrados no sistema e utiliza a foto do aluno para compor sua identificação.

O acesso à carteirinha é protegido por sessão, impedindo que usuários não autenticados acessem diretamente essa página.

### Geração de QR Code

Cada aluno possui um QR Code gerado automaticamente durante o cadastro.

O código é criado utilizando a biblioteca `qrcode` e contém informações como:

* Nome;
* RA;
* Curso;
* Turma.

O arquivo gerado é armazenado no diretório de QR Codes da aplicação.

### Upload de foto

Durante o cadastro, o usuário pode enviar uma foto para utilização na carteirinha.

A aplicação realiza uma validação das extensões permitidas e utiliza `secure_filename` para tratar o nome do arquivo antes de armazená-lo.

## Backend

O backend foi desenvolvido em **Python utilizando Flask**.

A aplicação possui diferentes rotas responsáveis por:

* Página inicial;
* Página sobre;
* Cadastro;
* Login;
* Logout;
* Carteirinha digital.

O Flask também é responsável pelo processamento dos formulários, autenticação, gerenciamento de sessões e comunicação com o banco de dados.

## Banco de dados

A aplicação utiliza **Flask-SQLAlchemy** para trabalhar com o banco de dados.

Foi criado um modelo `Aluno` contendo campos para identificação e informações acadêmicas, incluindo nome, usuário, RA, telefone, curso, turma, foto e senha.

O projeto utiliza SQLite durante o desenvolvimento local e está preparado para utilizar PostgreSQL por meio da variável de ambiente `DATABASE_URL` em ambientes de deploy.

A criação das tabelas é realizada por meio do script `create_db.py`, utilizando o contexto da aplicação Flask e o método `db.create_all()`.

## Arquitetura da aplicação

O projeto possui uma separação entre:

```text
projeto-senai-alunos/
├── static/
│   ├── uploads/
│   └── qrcodes/
├── templates/
├── app.py
├── create_db.py
├── requirements.txt
└── README.md
```

### `app.py`

Responsável pela aplicação Flask, rotas, autenticação, sessões, modelo de dados, upload de arquivos e geração dos QR Codes.

### `templates/`

Contém as páginas HTML utilizadas pela aplicação.

### `static/`

Armazena os arquivos estáticos e os arquivos gerados pela aplicação, incluindo imagens enviadas pelos alunos e QR Codes.

### `create_db.py`

Responsável pela criação das tabelas do banco de dados.

## Tecnologias utilizadas

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* HTML5
* CSS3
* JavaScript
* SQLite
* PostgreSQL
* QR Code
* Werkzeug
* Git
* GitHub
* Render

## Conceitos aplicados

* Desenvolvimento Full Stack;
* Arquitetura cliente-servidor;
* Rotas e requisições HTTP;
* Templates HTML;
* Formulários;
* Autenticação;
* Gerenciamento de sessões;
* Hash de senhas;
* ORM;
* Modelagem de dados;
* Banco de dados relacional;
* Upload e validação de arquivos;
* Geração dinâmica de QR Codes;
* Variáveis de ambiente;
* Deploy de aplicação web.

## Segurança

O projeto aplica algumas práticas básicas de segurança, como:

* Armazenamento das senhas utilizando hash;
* Validação das credenciais durante o login;
* Controle de acesso utilizando sessões;
* Validação das extensões dos arquivos enviados;
* Utilização de `secure_filename` para tratamento dos nomes dos arquivos;
* Utilização de variável de ambiente para configurações sensíveis.

## Deploy

A aplicação está hospedada no **Render** e possui configuração para utilização de banco de dados por variável de ambiente.

A aplicação também possui configuração para utilizar SQLite em ambiente local, permitindo desenvolvimento sem depender de um banco externo.

## Aprendizados

O desenvolvimento deste projeto permitiu aplicar conceitos de desenvolvimento Full Stack em uma aplicação funcional, indo além da construção da interface.

Durante o desenvolvimento foram trabalhados conceitos de backend com Flask, integração com banco de dados, autenticação, gerenciamento de sessões, segurança de senhas, upload de arquivos, geração de QR Codes e deploy.

O projeto também proporcionou experiência na organização de uma aplicação que integra diferentes camadas e serviços para entregar uma funcionalidade completa ao usuário.

## Status

**Projeto finalizado**

O sistema possui cadastro, autenticação, carteirinha digital, geração de QR Code, armazenamento de dados e deploy online.

## Autora

**Stefany Viveiros Barboza**

Estudante de Análise e Desenvolvimento de Sistemas e Engenharia da Computação, com interesse em desenvolvimento Full Stack, Inteligência Artificial, automação e construção de soluções digitais.
