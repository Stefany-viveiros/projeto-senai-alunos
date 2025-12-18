import mysql from 'mysql2';

const conexao = mysql.createConnection({
    host:'localhost',
    port:'3306',
    user:'root',
    password: 'root',
    database:'cadastro_pessoas'
});

conexao.connect();
export default conexao;