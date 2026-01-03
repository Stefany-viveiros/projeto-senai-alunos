from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta'  # necessário para sessão e flash

# Banco temporário de usuários
usuarios = {}  # Exemplo de estrutura:
# usuarios = {
#     'fernando': {
#         'senha': '123456',
#         'nome': 'Fernando Moreira',
#         'ra': '251488',
#         'telefone': '11999999999'
#     }
# }

# -------------------- ROTAS --------------------

# Home (index.html)
@app.route('/')
def home():
    return render_template('index.html')


# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        usuario = request.form['usuario']
        ra = request.form['ra']
        telefone = request.form['telefone']
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']

        # Validação
        if not nome or not usuario or not ra or not telefone or not senha or not senha_confirm:
            flash('Preencha todos os campos', 'erro')
            return redirect(url_for('cadastro'))

        if senha != senha_confirm:
            flash('As senhas não coincidem', 'erro')
            return redirect(url_for('cadastro'))

        if usuario in usuarios:
            flash('Usuário já cadastrado', 'erro')
            return redirect(url_for('cadastro'))

        # Salvar usuário completo
        usuarios[usuario] = {
            'senha': senha,
            'nome': nome,
            'ra': ra,
            'telefone': telefone
        }

        flash('Cadastro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            session['usuario'] = usuario  # salva usuário logado
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
    flash('Você saiu da conta', 'sucesso')
    return redirect(url_for('login'))


# Carteirinha
@app.route('/carteirinha')
def carteirinha():
    if 'usuario' not in session:
        flash('Faça login para acessar a carteirinha', 'erro')
        return redirect(url_for('login'))

    # Dados do usuário logado
    aluno = usuarios[session['usuario']]
    aluno['curso'] = 'Desenvolvimento de Sistemas'  # fixo
    aluno['turma'] = 'DS-1'                         # fixo

    return render_template('carteirinha.html', aluno=aluno)


# Sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


# -------------------- RODAR APP --------------------
if __name__ == '__main__':
    app.run(debug=True)