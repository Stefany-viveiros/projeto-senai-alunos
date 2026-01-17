from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import qrcode

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_senai'

# ================= CONFIGURAÇÕES =================
UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DATABASE = 'alunos.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# ================= BANCO DE DADOS =================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            ra TEXT NOT NULL,
            telefone TEXT NOT NULL,
            curso TEXT NOT NULL,
            turma TEXT NOT NULL,
            foto TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= FUNÇÕES AUXILIARES =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gerar_qr_code(usuario, aluno):
    conteudo = f"""
Nome: {aluno['nome']}
RA: {aluno['ra']}
Curso: {aluno['curso']}
Turma: {aluno['turma']}
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
        nome = request.form['nome']
        usuario = request.form['usuario']
        ra = request.form['ra']
        telefone = request.form['telefone']
        curso = request.form['curso']
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']
        foto = request.files['foto']

        if senha != senha_confirm:
            flash('As senhas não conferem.', 'erro')
            return redirect(url_for('cadastro'))

        if not allowed_file(foto.filename):
            flash('Foto inválida.', 'erro')
            return redirect(url_for('cadastro'))

        filename = secure_filename(foto.filename)
        foto.save(os.path.join(UPLOAD_FOLDER, filename))

        senha_hash = generate_password_hash(senha)

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alunos (nome, usuario, ra, telefone, curso, turma, foto, senha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, usuario, ra, telefone, curso, 'DS-2025', filename, senha_hash))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            flash('Usuário já cadastrado.', 'erro')
            return redirect(url_for('cadastro'))

        aluno = {
            'nome': nome,
            'ra': ra,
            'curso': curso,
            'turma': 'DS-2025'
        }

        gerar_qr_code(usuario, aluno)

        flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE usuario = ?", (usuario,))
        aluno = cursor.fetchone()
        conn.close()

        if not aluno or not check_password_hash(aluno['senha'], senha):
            flash('Usuário ou senha inválidos.', 'erro')
            return redirect(url_for('login'))

        session['usuario'] = aluno['usuario']
        session['nome'] = aluno['nome']

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

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE usuario = ?", (session['usuario'],))
    aluno = cursor.fetchone()
    conn.close()

    return render_template('carteirinha.html', aluno=aluno)

# ================= EXECUÇÃO =================
if __name__ == '__main__':
    app.run(debug=True)
