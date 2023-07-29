import os 
import sqlite3
from prettytable import PrettyTable

def LimparTerminal(): # limpar terminal
    os.system('cls' if os.name == 'nt' else 'clear')

con = sqlite3.connect("db.db") #conexão com o banco de dados
cursor = con.cursor()

def CadastrarEntrada():
    #capturar os dados da Entrada:
    print("Preencha os dados da nova entrada: \n")
    nome = input("Nome da entrada: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")
    ################################

    cursor.execute(f'INSERT INTO "main"."Entradas" ("nome", "valor", "categoria", "data") VALUES ("{nome}", "{valor}", "{categoria}", "{data}");')
    con.commit() #salvar no banco de dados

def CadastrarSaida():
    #capturar os dados da saida:
    print("Preencha os dados da nova saída: \n")
    nome = input("Nome da saída: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")
    #############################

    cursor.execute(f'INSERT INTO "main"."Saidas" ("nome", "valor", "categoria", "data") VALUES ("{nome}", "{valor}", "{categoria}", "{data}");')
    con.commit() #salvar no banco de dados

def CadastrarInvestimento():
    #capturar os dados do investimento:
    print("Preencha os dados do novo investimento: \n")
    nome = input("Nome do investimento: ")
    valor = input("Valor: ")
    tipo = input("tipo: ")
    qtd = input("Quantidade: ")
    data = input("Data: ")
    ##################################

    cursor.execute(f'INSERT INTO "main"."Investimentos" ("nome", "valor", "tipo", "quantidade", "data") VALUES ("{nome}", "{valor}", "{tipo}", "{qtd}", "{data}");')
    con.commit() #salvar no banco de dados

def GerarRelatorio():
    menu = input('''
 Oque deseja fazer?
                 
 1: Mostrar todas as entradas 
 2: Mostrar todas as saidas
 3: Mostrar todos os investimentos \n
 4: Mostrar a soma de todos
 → ''')
    if menu == "1":
        LimparTerminal()
        cursor.execute("SELECT * FROM Entradas")
        MyTableEntrada = PrettyTable(["ID", "Nome", "Valor", "Categoria", "Data"])
        data = cursor.fetchall()
        for i in data: 
            MyTableEntrada.add_row([i[0], i[1], i[2], i[3], i[4]])
        print("Dados da tabela entrada: \n")
        print(MyTableEntrada)
        input("\n\nprecione alguma tecla para sair ")
    if menu == "2":
        LimparTerminal()
        cursor.execute("SELECT * FROM Saidas")
        MyTableEntrada = PrettyTable(["ID", "Nome", "Valor", "Categoria", "Data"])
        data = cursor.fetchall()
        for i in data: 
            MyTableEntrada.add_row([i[0], i[1], i[2], i[3], i[4]])
        print("Dados da tabela saídas: \n")
        print(MyTableEntrada)
        input("\n\nprecione alguma tecla para sair ")
    if menu == "3":
        LimparTerminal()
        cursor.execute("SELECT * FROM Investimentos")
        MyTableEntrada = PrettyTable(["ID", "Nome", "Valor", "Tipo", "Quantidade", "Data"])
        data = cursor.fetchall()
        for i in data: 
            MyTableEntrada.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])
        print("Dados da tabela saídas: \n")
        print(MyTableEntrada)
        input("\n\nprecione alguma tecla para sair ")
    if menu == "4":
        LimparTerminal()
        cursor.execute("SELECT SUM(valor) FROM Entradas")
        print(f"Entrada: R${cursor.fetchall()[0][0] if cursor.fetchall()[0][0] == None else '0'}")
        cursor.execute("SELECT SUM(valor) FROM Saidas")
        print(f"Saídas: R${cursor.fetchall()[0][0] if cursor.fetchall()[0][0] != None else '0'}")
        cursor.execute("SELECT SUM(valor) FROM Investimentos")
        print(f"Investimentos: R${cursor.fetchall()[0][0] if cursor.fetchall()[0][0] != None else '0'}")
        input("\n\nprecione alguma tecla para sair ")
    LimparTerminal()
