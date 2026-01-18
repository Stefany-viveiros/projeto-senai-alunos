from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import qrcode

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_senai'

# ================= CONFIGURAÇÕES =================
UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# ================= CONFIGURAÇÃO MYSQL =================
# Substitua usuário, senha e database pelos seus
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senha@localhost/senai_alunos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODELO =================
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    ra = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(50), nullable=False, default='DS-2025')
    foto = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

# ================= FUNÇÕES AUXILIARES =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gerar_qr_code(usuario, aluno):
    conteudo = f"""
Nome: {aluno.nome}
RA: {aluno.ra}
Curso: {aluno.curso}
Turma: {aluno.turma}
"""
    qr = qrcode.make(conteudo)
    qr.save(os.path.join(QR_FOLDER, f"{usuario}.png"))

# ================= ROTAS =================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# ================= CADASTRO =================
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        usuario = request.form.get('usuario')
        ra = request.form.get('ra')
        telefone = request.form.get('telefone')
        curso = request.form.get('curso')
        senha = request.form.get('senha')
        senha_confirm = request.form.get('senha_confirm')
        foto = request.files.get('foto')

        if Aluno.query.filter_by(usuario=usuario).first():
            flash('Usuário já cadastrado.', 'erro')
            return redirect(url_for('cadastro'))

        if senha != senha_confirm:
            flash('As senhas não conferem.', 'erro')
            return redirect(url_for('cadastro'))

        if not foto or not allowed_file(foto.filename):
            flash('Foto inválida.', 'erro')
            return redirect(url_for('cadastro'))

        filename = secure_filename(foto.filename)
        foto.save(os.path.join(UPLOAD_FOLDER, filename))

        aluno = Aluno(
            nome=nome,
            usuario=usuario,
            ra=ra,
            telefone=telefone,
            curso=curso,
            foto=filename,
            senha=generate_password_hash(senha)
        )
        db.session.add(aluno)
        db.session.commit()

        gerar_qr_code(usuario, aluno)

        flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        aluno = Aluno.query.filter_by(usuario=usuario).first()

        if not aluno or not check_password_hash(aluno.senha, senha):
            flash('Usuário ou senha inválidos.', 'erro')
            return redirect(url_for('login'))

        session['usuario'] = aluno.usuario
        session['nome'] = aluno.nome

        flash('Login realizado com sucesso!', 'sucesso')
        return redirect(url_for('home'))

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta.', 'sucesso')
    return redirect(url_for('login'))

# ================= CARTEIRINHA =================
@app.route('/carteirinha')
def carteirinha():
    if 'usuario' not in session:
        flash('Faça login para acessar a carteirinha.', 'erro')
        return redirect(url_for('login'))

    aluno = Aluno.query.filter_by(usuario=session['usuario']).first()
    return render_template('carteirinha.html', aluno=aluno)

# ================= EXECUÇÃO =================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria as tabelas se não existirem
    app.run(debug=True)
