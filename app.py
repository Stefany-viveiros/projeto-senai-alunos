from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import qrcode

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta'

# ================= CONFIGURAÇÕES =================
UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar pastas se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= "BANCO DE DADOS" (MEMÓRIA) =================
usuarios = {}

# ================= QR CODE =================
def gerar_qr_code(usuario, aluno):
    conteudo = f"Nome: {aluno['nome']}\nRA: {aluno['ra']}\nCurso: {aluno['curso']}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(conteudo)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    filename = f"{usuario}.png"
    caminho = os.path.join(QR_FOLDER, filename)
    img.save(caminho)

    aluno['qr_code'] = filename

# ================= SESSÃO =================
@app.before_request
def check_session():
    if 'usuario' in session and session['usuario'] not in usuarios:
        session.clear()

def get_nome_logado():
    usuario = session.get('usuario')
    if usuario in usuarios:
        return usuarios[usuario]['nome']
    return "Visitante"

# ================= ROTAS =================
@app.route('/')
def home():
    nome = get_nome_logado()
    return render_template('index.html', nome=nome)

@app.route('/sobre')
def sobre():
    nome = get_nome_logado()
    return render_template('sobre.html', nome=nome)

# ================= CADASTRO =================
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    nome_logado = get_nome_logado()

    if request.method == 'POST':
        nome = request.form.get('nome')
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        ra = request.form.get('ra')
        curso = request.form.get('curso')

        if usuario in usuarios:
            flash('Usuário já existe')
            return redirect(url_for('cadastro'))

        usuarios[usuario] = {
            'nome': nome,
            'senha': senha,
            'ra': ra,
            'curso': curso
        }

        gerar_qr_code(usuario, usuarios[usuario])

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template('cadastro.html', nome=nome_logado)

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!')
            return redirect(url_for('home'))

        flash('Usuário ou senha inválidos')

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema')
    return redirect(url_for('home'))

# ================= PERFIL =================
@app.route('/perfil')
def perfil():
    usuario = session.get('usuario')

    if not usuario:
        return redirect(url_for('login'))

    aluno = usuarios.get(usuario)
    return render_template('perfil.html', aluno=aluno)

# ================= INICIAR SERVIDOR =================
if __name__ == "__main__":
    app.run(debug=True)
