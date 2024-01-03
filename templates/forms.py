from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, IntegerField, HiddenField, FloatField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder" : "Usuário"})
    email = EmailField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder" : "E-mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder" : "Senha"})
    submit = SubmitField("Cadastrar")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder" : "Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder" : "Senha"})
    submit = SubmitField("login")
    

class ModalBoxFormEntrada(FlaskForm):
    nome = StringField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder" : "nome"})
    tipo = HiddenField()
    valor = FloatField(validators=[InputRequired()], render_kw={"placeholder" : "valor"})
    data = DateField(validators=[InputRequired()])
    categoria = SelectField(validators=[InputRequired()], choices=['Salário', 'Venda de Serviços', 'Venda de Produtos', 'Dividendos'], render_kw={"placeholder" : "categoria"})
    descricao = StringField(validators=[InputRequired()], render_kw={"placeholder" : "descrição"})
    submit = SubmitField("Salvar")

class ModalBoxFormSaida(FlaskForm):
    nome = StringField(validators=[InputRequired(), Length(min=3, max=50)], render_kw={"placeholder" : "nome"})
    tipo = HiddenField()
    valor = FloatField(validators=[InputRequired()], render_kw={"placeholder" : "valor"})
    data = DateField(validators=[InputRequired()])
    categoria = SelectField(validators=[InputRequired()], choices=['Aluguel', 'Conta de Energia', 'Água', 'Gás', 'Condomínio', 'Cartão de Crédito', 'Viagem', 'Transporte', 'Streaming', 'Seguro de Carro'], render_kw={"placeholder" : "categoria"})
    descricao = StringField(validators=[InputRequired()], render_kw={"placeholder" : "descrição"})
    submit = SubmitField("Salvar")

class ModalBoxFormInvestimento(FlaskForm):
    nome = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    ativo = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    tipo = HiddenField()
    valor = FloatField(validators=[InputRequired()])
    data = DateField(validators=[InputRequired()])
    quantidade = IntegerField(validators=[InputRequired()])
    categoria = SelectField(validators=[InputRequired()], choices=["renda fixa", "renda variavel", "fii", "brd", "etf", "criptomoedas"])
    descricao = StringField(validators=[InputRequired()])
    submit = SubmitField("Salvar")

class EditarForm(FlaskForm):
    nome = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    valor = FloatField(validators=[InputRequired()])
    data = DateField(validators=[InputRequired()])
    tipo = SelectField(choices=['entrada', 'saida', 'investimento'], validators=[InputRequired()])
    categoria = SelectField(choices=['salario', 'venda de serviço', 'venda de produto','compra', 'renda fixa', 'renda variavel', 'fii', 'brd', 'etf', 'criptomoedas'], validators=[InputRequired()])
    quantidade = IntegerField(validators=[InputRequired()])
    descricao = StringField(validators=[InputRequired()])
    submit = SubmitField("Salvar")

class VenderForm(FlaskForm):
    nome = HiddenField()
    preco_compra = HiddenField()
    id = HiddenField()
    data_venda = DateField(validators=[InputRequired()])
    preco_venda = FloatField(validators=[InputRequired()])
    quantidade = IntegerField(validators=[InputRequired()])
    submit = SubmitField("Vender")
