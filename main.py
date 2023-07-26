from entities.functions import Functions

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
    