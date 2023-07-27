import os 

def CadastrarEntrada():
    os.system('cls' if os.name == 'nt' else 'clear') # limpar terminal
    print("Preencha os dados da nova entrada: \n")
    nome = input("Nome da entrada: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")

def CadastrarSaida():
    os.system('cls' if os.name == 'nt' else 'clear') # limpar terminal
    print("Preencha os dados da nova saída: \n")
    nome = input("Nome da saída: ")
    valor = input("Valor: ")
    categoria = input("Categoria: ")
    data = input("Data: ")

def CadastrarInvestimento():
    os.system('cls' if os.name == 'nt' else 'clear') # limpar terminal
    print("Preencha os dados do novo investimento: \n")
    nome = input("Nome do investimento: ")
    valor = input("Valor: ")
    tipo = input("tipo: ")
    data = input("Data: ")