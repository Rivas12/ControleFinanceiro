import os 
import sqlite3

def LimparTerminal(): # limpar terminal
    os.system('cls' if os.name == 'nt' else 'clear')

con = sqlite3.connect("db.db") #conexão com o banco de dados
cursor = con.cursor()

def CadastrarEntrada():
    LimparTerminal()
    print("Preencha os dados da nova entrada: \n")
    nome = input("Nome da entrada: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")

    cursor.execute(f'INSERT INTO "main"."Entradas" ("nome", "valor", "categoria", "data") VALUES ("{nome}", "{valor}", "{categoria}", "{data}");')
    con.commit()
    LimparTerminal()

def CadastrarSaida():
    LimparTerminal()
    print("Preencha os dados da nova saída: \n")
    nome = input("Nome da saída: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")
    cursor.execute(f'INSERT INTO "main"."Saidas" ("nome", "valor", "categoria", "data") VALUES ("{nome}", "{valor}", "{categoria}", "{data}");')
    con.commit()
    LimparTerminal()

def CadastrarInvestimento():
    LimparTerminal()
    print("Preencha os dados do novo investimento: \n")
    nome = input("Nome do investimento: ")
    valor = input("Valor: ")
    tipo = input("tipo: ")
    data = input("Data: ")
    LimparTerminal()