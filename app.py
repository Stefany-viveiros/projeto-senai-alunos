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

# ================= BANCO DE DADOS =================
usuarios = {}

# ================= QR CODE =================
def gerar_qr_code(usuario, aluno):
    conteudo = f"Nome: {aluno['nome']}\nRA: {aluno['ra']}\nCurso: {aluno['curso']}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(conteudo)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    # Salvar apenas o nome do arquivo
    filename = f"{usuario}.png"
    caminho = os.path.join(QR_FOLDER, filename)
    img.save(caminho)

    aluno['qr_code'] = filename

# ================= ROTAS =================

@app.before_request
def check_session():
    # Se a sessão tiver usuário inválido, limpa
    if 'usuario' in session and session['usuario'] not in usuarios:
        session.clear()

@app.route('/')
def home():
    return render_template('index.html', usuario=session.get('usuario'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html', usuario=session.get('usuario'))

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

        if not all([nome, usuario, ra, telefone, curso, senha, senha_confirm]):
            flash('Preencha todos os campos', 'erro')
            return redirect(url_for('cadastro'))

        if senha != senha_confirm:
            flash('As senhas não coincidem', 'erro')
            return redirect(url_for('cadastro'))

        if usuario in usuarios:
            flash('Usuário já cadastrado', 'erro')
            return redirect(url_for('cadastro'))

        if not foto or foto.filename == '':
            flash('Selecione uma foto', 'erro')
            return redirect(url_for('cadastro'))

        if not allowed_file(foto.filename):
            flash('Formato de imagem inválido', 'erro')
            return redirect(url_for('cadastro'))

        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Salvar usuário
        usuarios[usuario] = {
            'nome': nome,
            'senha': senha,
            'ra': ra,
            'telefone': telefone,
            'curso': curso,
            'foto': filename,
            'turma': 'DS-1'
        }

        gerar_qr_code(usuario, usuarios[usuario])
        flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html', usuario=session.get('usuario'))

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario not in usuarios:
            flash('Usuário não cadastrado', 'erro')
        elif usuarios[usuario]['senha'] != senha:
            flash('Usuário ou senha incorretos', 'erro')
        else:
            session['usuario'] = usuario
            flash(f'Bem-vindo, {usuarios[usuario]["nome"]}!', 'sucesso')
            return redirect(url_for('home'))

    return render_template('login.html', usuario=session.get('usuario'))

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect(url_for('home'))

# ================= CARTEIRINHA =================
@app.route('/carteirinha')
def carteirinha():
    usuario = session.get('usuario')
    if not usuario or usuario not in usuarios:
        flash('Faça login para acessar a carteirinha', 'erro')
        return redirect(url_for('login'))

    aluno = usuarios[usuario]
    return render_template('carteirinha.html', aluno=aluno, usuario=usuario)

# ================= EXECUÇÃO =================
if __name__ == '__main__':
    app.run(debug=True)
