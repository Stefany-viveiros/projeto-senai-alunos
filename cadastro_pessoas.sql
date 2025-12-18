create database cadastro_pessoas;

create table pessoas(
	id int auto_increment primary key,
    nome varchar(100) not null,
    email varchar (100) not null,
    nascimento int (10) not null,
	endereco varchar(100) not null,
    bairro varchar (50) not null,
    cidade varchar(50) not null,
    estado varchar(50) not null,
    cep int (20) not null,
    celular int (20) not null
);