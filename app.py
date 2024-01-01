from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt, check_password_hash
from datetime import datetime, date

from templates.forms import *

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(20), nullable = False)

class Movimentacoes(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer)
    nome = db.Column(db.String(50), nullable = False)
    ativo = db.Column(db.String(10), nullable = True)
    tipo = db.Column(db.String(20), nullable = False)
    valor = db.Column(db.Float(20), nullable = False)
    quantidade = db.Column(db.Integer, nullable = True)
    categoria = db.Column(db.String(20), nullable = False)
    descricao = db.Column(db.String(100), nullable = False)
    data = db.Column(db.Date)

class InvestimentosVendidos(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer)
    nome = db.Column(db.String(50), nullable = False)
    valor_compra = db.Column(db.Float(20), nullable = False)
    data_venda = db.Column(db.Date, nullable = False)
    valor_venda = db.Column(db.Float(20), nullable = False)
    quantidade_venda = db.Column(db.Integer, nullable = True)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form = form)

@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('cadastrar.html', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    form_vender_investimento = VenderForm()
    data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id))
    if len(list(data)) == 0:
        data = 0
    else:
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id))
    return render_template('index.html', page = "dashboard", data = data, form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, form_vender_investimento = form_vender_investimento)

@app.route('/entradas', methods = ['GET', 'POST'])
@login_required
def entrada():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    form_vender_investimento = VenderForm()
    data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "entrada"))
    if len(list(data)) == 0:
        data = 0
    else:
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "entrada"))
    if form_entrada.validate_on_submit():
        tipo = "entrada"
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_entrada.nome.data, tipo = tipo, valor = form_entrada.valor.data, categoria = form_entrada.categoria.data, descricao = form_entrada.descricao.data, data = form_entrada.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('index.html', data = data, page = "entrada",  form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, form_vender_investimento = form_vender_investimento)

@app.route('/saidas')
@login_required
def saida():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    form_vender_investimento = VenderForm()
    data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "saida"))
    if len(list(data)) == 0:
        data = 0
    else:
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "saida"))
    return render_template('index.html', data = data,  form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, form_vender_investimento = form_vender_investimento, page = "saida")

@app.route('/investimentos')
@login_required
def investimentos():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    form_vender_investimento = VenderForm()
    data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "investimento"))
    if len(list(data)) == 0:
        data = 0
    else:
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "investimento"))
    return render_template('index.html', data = data,  form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, form_vender_investimento = form_vender_investimento, page = "investimento")

@app.route('/venderinvestimento', methods = ['POST', 'GET'])
@login_required
def venderinvestimento():
    form_vender_investimento = VenderForm()
    if form_vender_investimento.validate_on_submit():
        Movimentacoes.query.filter_by(id_user = current_user.id, id = form_vender_investimento.id.data).delete()
        nova_venda = InvestimentosVendidos(id_user = current_user.id, nome = form_vender_investimento.nome.data, valor_compra = form_vender_investimento.preco_compra.data, data_venda = form_vender_investimento.data_venda.data, valor_venda = str(form_vender_investimento.preco_venda.data).replace(',','.'), quantidade_venda = form_vender_investimento.quantidade.data)
        db.session.add(nova_venda)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/cadastrar/movimentacao', methods = ['POST', 'GET'])
@login_required
def cadastrar_movimentacao():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    if form_entrada.validate_on_submit():
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_entrada.nome.data, tipo = form_entrada.tipo.data, valor = form_entrada.valor.data, categoria = form_entrada.categoria.data, descricao = form_entrada.descricao.data, data = form_entrada.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
    elif form_saida.validate_on_submit():
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_saida.nome.data, tipo = form_saida.tipo.data, valor = form_saida.valor.data, categoria = form_saida.categoria.data, descricao = form_saida.descricao.data, data = form_saida.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
    elif form_investimento.validate_on_submit():
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_investimento.nome.data,ativo = form_investimento.ativo.data, tipo = form_investimento.tipo.data, quantidade = form_investimento.quantidade.data, valor = form_investimento.valor.data, categoria = form_investimento.categoria.data, descricao = form_investimento.descricao.data, data = form_investimento.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/deletar', methods = ['POST', 'GET'])
@login_required
def deletar():
    Movimentacoes.query.filter_by(id_user = current_user.id, id = request.args["id"]).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/editar', methods = ['POST', 'GET'])
@login_required
def editar():
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    editarform = EditarForm()
    form_vender_investimento = VenderForm()
    data = Movimentacoes.query.filter_by(id_user = current_user.id, id = request.args["id"])

    if editarform.validate_on_submit():
        updates = dict(nome = editarform.nome.data, 
                       valor = editarform.valor.data,
                       tipo = editarform.tipo.data,
                       categoria = editarform.categoria.data,
                       data = datetime.strptime(str(editarform.data.data), '%Y-%m-%d'),
                       descricao = editarform.descricao.data)
        print("passou")
        Movimentacoes.query.filter_by(id_user = current_user.id, id = request.args["id"]).update(updates)
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template("editar.html", page = "dashboard", data = data,  form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, editarform = editarform, form_vender_investimento = form_vender_investimento)

if __name__ == "__main__":
    app.run(debug=True)