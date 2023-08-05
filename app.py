from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect("db.db", check_same_thread=False) #conexão com o banco de dados
cursor = con.cursor()


app = Flask(__name__)

@app.route('/')
def home():
    return redirect("http://localhost:5000/entradas")

@app.route('/entradas')
def entrada():
    cursor.execute("SELECT * FROM Entradas")
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "entrada")

@app.route('/saidas')
def saida():
    cursor.execute("SELECT * FROM Saidas")
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "saida")

@app.route('/investimentos')
def investimentos():
    cursor.execute("SELECT * FROM Investimentos")
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "investimento")

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html', page = "relatorio")

@app.route('/cadastrar/entrada', methods = ['POST'])
def cadastrarEntrada():
    cursor.execute(f'INSERT INTO "main"."Entradas" ("nome", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/entradas")

@app.route('/cadastrar/saida', methods = ['POST'])
def cadastrarSaida():
    cursor.execute(f'INSERT INTO "main"."Saidas" ("nome", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/saidas")

@app.route('/cadastrar/investimento', methods = ['POST'])
def cadastrarInvestimento():
    cursor.execute(f'INSERT INTO "main"."Investimentos" ("nome", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/investimentos")

if __name__ == "__main__":
    app.run(debug=True)