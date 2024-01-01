from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, desc, asc
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
    return db.session.get(User, user_id)

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
    print(current_user.id)
    form_entrada = ModalBoxFormEntrada()
    form_saida = ModalBoxFormSaida()
    form_investimento = ModalBoxFormInvestimento()
    form_vender_investimento = VenderForm()
    dict_distribuicao = {
        'ativos': db.session.execute(select(Movimentacoes.nome, Movimentacoes.valor * Movimentacoes.quantidade).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == 'investimento')).all(),
        'patrimonio': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where((Movimentacoes.id_user == current_user.id) & ((Movimentacoes.tipo == 'investimento') | (Movimentacoes.tipo == 'entrada')))).scalar(),
        'total_investido': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento')).scalar(),
        'total_dividendos': db.session.execute(select(func.coalesce(func.sum(Movimentacoes.valor * Movimentacoes.quantidade), 0)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'entrada',Movimentacoes.categoria == 'dividendo')).scalar() + round(db.session.execute(func.coalesce(select(func.sum((InvestimentosVendidos.valor_venda - InvestimentosVendidos.valor_compra) * InvestimentosVendidos.quantidade_venda)).where(Movimentacoes.id_user == current_user.id), 0)).scalar(), 2),
        'renda fixa': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'renda fixa')).scalar(),
        'renda variavel': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'renda variavel')).scalar(),
        'fii': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'fii')).scalar(),
        'etf': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'etf')).scalar(),
        'brd': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'brd')).scalar(),
        'criptomoedas': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento',Movimentacoes.categoria == 'criptomoedas')).scalar(),
        'total_entradas': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'entrada')).scalar(),
        'total_saidas': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'saida')).scalar(),
        'total_investimentos': db.session.execute(select(func.sum(Movimentacoes.valor * Movimentacoes.quantidade)).where(Movimentacoes.id_user == current_user.id,Movimentacoes.tipo == 'investimento')).scalar()
    }
    # Substituir valores "None" por 0
    for chave, valor in dict_distribuicao.items():
        if valor is None:
            dict_distribuicao[chave] = 0
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id))
    return render_template('index.html', page = "dashboard", data = data, form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, form_vender_investimento = form_vender_investimento, dict_distribuicao = dict_distribuicao)

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
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "entrada").order_by(Movimentacoes.data.desc()))
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
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "saida").order_by(Movimentacoes.data.desc()))
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
        data = db.session.execute(select(Movimentacoes).where(Movimentacoes.id_user == current_user.id, Movimentacoes.tipo == "investimento").order_by(Movimentacoes.data.desc()))
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
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_entrada.nome.data, quantidade = 1, tipo = form_entrada.tipo.data, valor = form_entrada.valor.data, categoria = form_entrada.categoria.data, descricao = form_entrada.descricao.data, data = form_entrada.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
        return redirect(url_for('entrada'))
    elif form_saida.validate_on_submit():
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_saida.nome.data, quantidade = 1, tipo = form_saida.tipo.data, valor = form_saida.valor.data, categoria = form_saida.categoria.data, descricao = form_saida.descricao.data, data = form_saida.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
        return redirect(url_for('saida'))
    elif form_investimento.validate_on_submit():
        nova_movimentacao = Movimentacoes(id_user = current_user.id, nome = form_investimento.nome.data,ativo = form_investimento.ativo.data, tipo = form_investimento.tipo.data, quantidade = form_investimento.quantidade.data, valor = form_investimento.valor.data, categoria = form_investimento.categoria.data, descricao = form_investimento.descricao.data, data = form_investimento.data.data)
        db.session.add(nova_movimentacao)
        db.session.commit()
        return redirect(url_for('investimentos'))
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
    print(editarform.categoria.data)
    if editarform.validate_on_submit():
        print(editarform.quantidade.data)
        updates = dict(nome = editarform.nome.data, 
                       valor = editarform.valor.data,
                       tipo = editarform.tipo.data,
                       categoria = editarform.categoria.data,
                       quantidade = editarform.quantidade.data,
                       data = datetime.strptime(str(editarform.data.data), '%Y-%m-%d'),
                       descricao = editarform.descricao.data)
        print(editarform.quantidade.data)
        Movimentacoes.query.filter_by(id_user = current_user.id, id = request.args["id"]).update(updates)
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        print(editarform.errors)
        return render_template("editar.html", page = "dashboard", data = data,  form_entrada = form_entrada, form_saida = form_saida, form_investimento = form_investimento, editarform = editarform, form_vender_investimento = form_vender_investimento)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)