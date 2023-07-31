from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect("db.db", check_same_thread=False) #conexão com o banco de dados
cursor = con.cursor()


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('entrada.html')

@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    print(request.form["nome"])
    print(request.form["valor"])
    print(request.form["data"])
    print(request.form["categoria"])
    cursor.execute(f'INSERT INTO "main"."Entradas" ("nome", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/")


if __name__ == "__main__":
    app.run(debug=True)