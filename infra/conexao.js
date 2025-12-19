import mysql from 'mysql2/promise';

const conexao = mysql.createPool({
    host:'localhost',
    port:'3306',
    user:'root',
    password: '',
    database:'cadastro_pessoas',
    waitForConnections:true,
    connectionLimit:10,
    queueLimit:0
});

// conexao.connect();
export default conexao;