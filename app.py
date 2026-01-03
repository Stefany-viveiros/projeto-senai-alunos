from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta'

# Upload de fotos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar pasta uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Banco temporário
usuarios = {}

# ---------------- ROTAS ----------------

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Cadastro
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

        if not nome or not usuario or not ra or not telefone or not curso or not senha or not senha_confirm:
            flash('Preencha todos os campos', 'erro')
            return redirect(url_for('cadastro'))

        if senha != senha_confirm:
            flash('As senhas não coincidem', 'erro')
            return redirect(url_for('cadastro'))

        if usuario in usuarios:
            flash('Usuário já cadastrado', 'erro')
            return redirect(url_for('cadastro'))

        # Foto
        if 'foto' not in request.files:
            flash('Nenhuma foto selecionada', 'erro')
            return redirect(url_for('cadastro'))

        foto = request.files['foto']

        if foto.filename == '':
            flash('Nenhuma foto selecionada', 'erro')
            return redirect(url_for('cadastro'))

        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Formato de imagem inválido', 'erro')
            return redirect(url_for('cadastro'))

        # Salvar usuário
        usuarios[usuario] = {
            'senha': senha,
            'nome': nome,
            'ra': ra,
            'telefone': telefone,
            'curso': curso,
            'foto': filename,
            'turma': 'DS-1'  # pode ajustar se quiser dinamizar
        }

        flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            session['usuario'] = usuario
            flash(f'Bem-vindo, {usuarios[usuario]["nome"]}!', 'sucesso')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect(url_for('home'))


# Carteirinha
@app.route('/carteirinha')
def carteirinha():
    usuario = session.get('usuario')
    if not usuario:
        flash('Você precisa estar logado para acessar a carteirinha', 'erro')
        return redirect(url_for('login'))

    aluno = usuarios[usuario]
    return render_template('carteirinha.html', aluno=aluno)


if __name__ == '__main__':
    app.run(debug=True)
