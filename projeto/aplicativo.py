from flask import Flask, render_template, request, redirect, url_for, session
from db import criar_conexao, criar_tabelas
aplicativo = Flask(__name__)
aplicativo.config["SECRET_KEY"] = "livros"
criar_tabelas()
@aplicativo.route("/")
def index():
    return render_template("index.html")
@aplicativo.route("/pagina_cadastro", methods=["GET","POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        conexao = criar_conexao()
        conexao.execute(
            "INSERT INTO usuarios(nome) VALUES(?)",
            (nome,)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for("pagina_login"))
    return render_template("pagina_cadastro.html")
@aplicativo.route("/pagina_login", methods=["GET","POST"])
def pagina_login():
    if request.method == "POST":
        nome = request.form.get("nome")
        conexao = criar_conexao()
        resultado = conexao.execute(
            "SELECT * FROM usuarios WHERE nome=?",
            (nome,)
        )
        pessoa = resultado.fetchone()
        conexao.close()
        if pessoa:
            session["pessoa"] = pessoa["nome"]
            return redirect(url_for("livros_view"))
    return render_template("pagina_login.html")
@aplicativo.route("/logout")
def logout():
    session.pop("pessoa", None)
    return redirect(url_for("index"))
@aplicativo.route("/livros")
def livros_view():
    if "pessoa" not in session :
        return redirect(url_for("pagina_login"))
    conexao = criar_conexao()
    genero = request.args.get("genero")
    if genero:
        resultado = conexao.execute(
            "SELECT * FROM livros WHERE genero=?",
            (genero,)
        )
    else:
        resultado = conexao.execute(
            "SELECT * FROM livros"
        )
    livros = resultado.fetchall()
    conexao.close()
    return render_template(
        "book.html",
        livros=livros
    )
@aplicativo.route("/novo", methods=["GET","POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome")
        genero = request.form.get("genero")
        conexao = criar_conexao()
        conexao.execute(
            "INSERT INTO livros(nome, genero) VALUES(?,?)",
            (nome, genero)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for("livros_view"))
    return render_template("pagina_novolivro.html")
@aplicativo.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    conexao = criar_conexao()
    if request.method == "POST":
        nome = request.form.get("nome")
        genero = request.form.get("genero")
        conexao.execute(
            "UPDATE livros SET nome=?, genero=? WHERE id=?",
            (nome, genero, id)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for("livros_view"))
    resultado = conexao.execute(
        "SELECT * FROM livros WHERE id=?",
        (id,)
    )
    livro = resultado.fetchone()
    conexao.close()
    return render_template(
        "editar_livro.html",
        livro=livro
    )
@aplicativo.route("/remover/<int:id>")
def remover(id):
    conexao = criar_conexao()
    conexao.execute(
        "DELETE FROM livros WHERE id=?",
        (id,)
    )
    conexao.commit()
    conexao.close()
    return redirect(url_for("livros_view"))
if __name__ == "__main__":
    aplicativo.run(debug=True)
