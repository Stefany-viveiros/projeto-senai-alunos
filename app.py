from flask import Flask, render_template, request, redirect, url_for, session
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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= "BANCO DE DADOS" =================
# (fica em memória — não some enquanto o servidor estiver rodando)
usuarios = {}

# ================= QR CODE =================

def gerar_qr_code(usuario, aluno):
    conteudo = f"Nome: {aluno['nome']}\nRA: {aluno['ra']}\nCurso: {aluno['curso']}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(conteudo)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    caminho = f'{QR_FOLDER}/{usuario}.png'
    img.save(caminho)

    aluno['qr_code'] = caminho

# ================= ROTAS =================

@app.route('/')
def home():
    return render_template(
        'index.html',
        usuario=session.get('usuario'),
        nome=session.get('nome')
    )

@app.route('/sobre')
def sobre():
    return render_template(
        'sobre.html',
        usuario=session.get('usuario'),
        nome=session.get('nome')
    )

# ================= CADASTRO =================

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = None
    sucesso = None

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
            erro = 'Preencha todos os campos'

        elif senha != senha_confirm:
            erro = 'As senhas não coincidem'

        elif usuario in usuarios:
            erro = 'Usuário já cadastrado'

        elif not foto or foto.filename == '':
            erro = 'Selecione uma foto'

        elif not allowed_file(foto.filename):
            erro = 'Formato de imagem inválido'

        else:
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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
            sucesso = 'Cadastro realizado com sucesso!'

    return render_template(
        'cadastro.html',
        erro=erro,
        sucesso=sucesso,
        usuario=session.get('usuario'),
        nome=session.get('nome')
    )

# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario not in usuarios:
            erro = 'Usuário não cadastrado'
        elif usuarios[usuario]['senha'] != senha:
            erro = 'Usuário ou senha incorretos'
        else:
            session['usuario'] = usuario
            session['nome'] = usuarios[usuario]['nome']
            return redirect(url_for('home'))

    return render_template(
        'login.html',
        erro=erro,
        usuario=session.get('usuario'),
        nome=session.get('nome')
    )

# ================= LOGOUT =================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ================= CARTEIRINHA =================

@app.route('/carteirinha')
def carteirinha():
    usuario = session.get('usuario')

    if not usuario:
        return redirect(url_for('login'))

    aluno = usuarios[usuario]

    return render_template(
        'carteirinha.html',
        aluno=aluno,
        usuario=session.get('usuario'),
        nome=session.get('nome')
    )

# ================= EXECUÇÃO =================

if __name__ == '__main__':
    app.run(debug=True)
