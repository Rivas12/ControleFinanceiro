from entities.functions import *

#Função responsavel pelo menu, assim que o usuario escolher a opção a função será executada
stop = False
while not stop:
    menus = input('''
 Selecione a opção desejada: 
                 
 1: Criar entrada
 2: Criar saída
 3: Criar investimento \n
 4: Relatorio
 → ''')
    LimparTerminal()
    if menus == "1":
        CadastrarEntrada()
    if menus == "2":
        CadastrarSaida()
    if menus == "3":
        CadastrarInvestimento()
    if menus == "4":
        GerarRelatorio()
    if menus == "5":
        break
    LimparTerminal()