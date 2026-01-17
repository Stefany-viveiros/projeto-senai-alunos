from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_super_secreta_123"

# ================= CONFIG ADMIN =================
ADMIN_EMAIL = "admin@senai.com"

# ================= BANCO =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

criar_tabelas()

# ================= DECORATORS =================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") != ADMIN_EMAIL:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

# ================= ROTAS =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha)
            )
            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Este email já está cadastrado.", "error")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@login_required
@admin_required
def admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template("admin.html", usuarios=usuarios)

@app.route("/carteirinha")
@login_required
def carteirinha():
    return "<h1>Carteirinha do Aluno</h1>"

# ================= EXEC =================
if __name__ == "__main__":
    app.run(debug=True)
