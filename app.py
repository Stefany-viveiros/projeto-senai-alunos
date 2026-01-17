from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import qrcode

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta'

# ================= CONFIG BANCO =================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'alunos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODELO =================
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    ra = db.Column(db.String(30), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    qr_code = db.Column(db.String(100))

# ================= QR CODE =================
QR_FOLDER = 'static/qrcodes'
os.makedirs(QR_FOLDER, exist_ok=True)

def gerar_qr_code(usuario, aluno):
    conteudo = f"Nome: {aluno.nome}\nRA: {aluno.ra}\nCurso: {aluno.curso}"
    qr = qrcode.make(conteudo)

    filename = f"{usuario}.png"
    caminho = os.path.join(QR_FOLDER, filename)
    qr.save(caminho)

    aluno.qr_code = filename
    db.session.commit()

# ================= ROTAS =================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']

        if Aluno.query.filter_by(usuario=usuario).first():
            flash('Usuário já existe', 'erro')
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(request.form['senha'])

        aluno = Aluno(
            nome=request.form['nome'],
            usuario=usuario,
            senha=senha_hash,
            ra=request.form['ra'],
            curso=request.form['curso']
        )

        db.session.add(aluno)
        db.session.commit()

        gerar_qr_code(usuario, aluno)

        flash('Cadastro realizado! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        aluno = Aluno.query.filter_by(usuario=usuario).first()

        if aluno and check_password_hash(aluno.senha, senha):
            session['usuario'] = aluno.usuario
            session['nome'] = aluno.nome
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    aluno = Aluno.query.filter_by(usuario=session['usuario']).first()
    return render_template('perfil.html', aluno=aluno)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= START =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
