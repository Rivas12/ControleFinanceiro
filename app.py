from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect("db.db", check_same_thread=False) #conexão com o banco de dados
cursor = con.cursor()


app = Flask(__name__)

@app.route('/')
def home():
    return redirect('http://localhost:5000/movimentacoes')

@app.route('/movimentacoes')
def movimentacoes():
    cursor.execute("SELECT * FROM Movimentacoes ORDER BY data DESC")
    data = cursor.fetchall()
    return render_template('index.html', page = "movimentacoes", contador = 0, data = data)

@app.route('/entradas')
def entrada():
    cursor.execute('SELECT * FROM Movimentacoes WHERE tipo == "entrada"')
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "entrada")

@app.route('/saidas')
def saida():
    cursor.execute('SELECT * FROM Movimentacoes WHERE tipo == "saida"')
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "saida")

@app.route('/investimentos')
def investimentos():
    cursor.execute('SELECT * FROM Movimentacoes WHERE tipo == "investimento"')
    data = cursor.fetchall()
    return render_template('index.html', data = data, page = "investimento")

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html', page = "relatorio")

@app.route('/cadastrar/entrada', methods = ['POST'])
def cadastrarEntrada():
    cursor.execute(f'INSERT INTO "main"."Movimentacoes" ("nome", "tipo", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "entrada", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/entradas")

@app.route('/cadastrar/saida', methods = ['POST'])
def cadastrarSaida():
    cursor.execute(f'INSERT INTO "main"."Movimentacoes" ("nome", "tipo", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "saida", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/saidas")

@app.route('/cadastrar/investimento', methods = ['POST'])
def cadastrarInvestimento():
    cursor.execute(f'INSERT INTO "main"."Movimentacoes" ("nome", "tipo", "valor", "categoria", "descricao", "data") VALUES ("{request.form["nome"]}", "investimento", "{request.form["valor"]}", "{request.form["categoria"]}", "{request.form["descricao"]}", "{request.form["data"]}");')
    con.commit() #salvar no banco de dados
    return redirect("http://localhost:5000/investimentos")

@app.route('/deletar', methods = ['GET'])
def deletar():
    cursor.execute(f'DELETE FROM Movimentacoes WHERE id == {request.args["id"]}')
    con.commit()
    return redirect("http://localhost:5000/movimentacoes")

@app.route('/editar', methods = ['POST', 'GET'])
def editar():
    if request.method == 'POST':
        cursor.execute(f'UPDATE Movimentacoes SET nome = "{request.form["nome"]}", valor = "{request.form["valor"]}" , categoria = "{request.form["categoria"]}", descricao = "{request.form["descricao"]}", data = "{request.form["data"]}" WHERE id == {request.args["id"]};')
        data = cursor.fetchall()
        return redirect("http://localhost:5000/movimentacoes")
    else:
        cursor.execute(f'SELECT * FROM Movimentacoes WHERE id == {request.args["id"]}')
        data = cursor.fetchall()
        return render_template('editar.html', data = data)

if __name__ == "__main__":
    app.run(debug=True)