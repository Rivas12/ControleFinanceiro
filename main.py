from entities.functions import *

#Função responsavel pelo menu, assim que o usuario escolher a opção a função será executada
stop = False
while not stop:
    menu = input('''
 Selecione a opção desejada: 
                 
 1: Criar entrada
 2: Criar saída
 3: Criar investimento \n
 4: sair
 → ''')
    if menu == "1":
        CadastrarEntrada()
    if menu == "2":
        CadastrarSaida()
    if menu == "3":
        CadastrarInvestimento()
    if menu == "4":
        break