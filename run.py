#-*- coding: utf-8 -*-
"""
Feito isto, leia o arquivo e imprima as seguintes informações:

Quem mais recebe e quem menos recebe na empresa e a média salarial da empresa
Quem mais recebe e quem menos recebe em cada área e a média salarial em cada área
A área com mais funcionários e a área com menos funcionários
Das pessoas que têm o mesmo sobrenome, aquela que recebe mais (não inclua sobrenomes que apenas uma pessoa tem nos resultados)
"""
import ijson
import os
import sys
import locale
import codecs

# abre o arquivo json
file_name = 'funcionarios-5M.json'
arquivo = open(file_name)
file_size = os.path.getsize(file_name)
# Aqui declaramos todas as variáveis que utilizaremos para armazenar os resultados desejados
# é interessante que o nome da variável seja bem descritivo, mesmo sendo maior.

# os funcionários que mais recebem e os que menos recebem, e a média salarial da empresa
# para calcular a média precisaremos da quantidade de funcionários (len(funcionarios))
# e a soma
funcionario_conta = 0
funcionario_mais_recebe = []
funcionario_menos_recebe = []
funcionario_soma_receita = 0
funcionario_media_receita = None
# os funcionários que mais recebem e os que menos recebem de CADA ÁREA, e a média salarial em cada área
# nesse caso utilizaremos um dict para armazenar o respectivo valor de cada área
# aqui podemos utilizar somente um dict, mas acredito que para alguns, didaticamente pode ser mais simples
# de entender de forma separada
funcionario_area_mais_recebe = {}
funcionario_area_menos_recebe = {}
funcionario_area_soma_receita = {}
funcionario_area_conta = {}
funcionatio_area_media_receita = {}
# área com mais funcionários e a área com menos funcionários
area_mais_funcionarios = None
area_menos_funcionarios = None
area_funcionarios_soma = {}
# para as pessoas que têm um mesmo sobrenome, utilizamos um dict novamente.
# assim associamos o respectivo valor para cada chave
# sobrenome_controle armazena uma lista de todos os sobrenomes para pesquisar se um sobrenome já foi visto
# sobrenome_controle_duplicados armazena a lista dos sobrenomes iguais. Percorremos essa variável para poder exibir os resultados
sobrenome_mais_recebe = {}
sobrenome_controle = []
sobrenome_controle_duplicados = []

# reorganiza as áreas para serem requisitadas por chave
areas = {}
for json_areas in ijson.items(arquivo, 'areas'):
    for area in json_areas:
        areas[area['codigo']] = area

arquivo.close()
arquivo = open(file_name)

# coletamos os dados dos funcionários
funcionario = {}

# vamos controlar o status para mostrar na tela
status = 0
line = 0
for prefix, the_type, value in ijson.parse(arquivo):
    # cada caracter tem um byte, então vamos dividir para atualizar
    # vamos suport que cada linha tem aproximadamente 36 bytes
    #line_size = 7 * line
    #status = (line_size * 100) / file_size
    #sys.stdout.write('{}%\r'.format(status))
    ##sys.stdout.flush()
    #line += 1

    if 'funcionarios.item' in prefix:
        key = prefix.replace('funcionarios.item.', '')
        funcionario[key] = value
        if the_type != 'end_map':
            continue
    else:
        continue

    # utilizamos bastante o campo salário do funcionário
    # então criamos uma variável para armazená-lo
    salario = funcionario['salario']
    # inicializamos os valores com o primeiro funcionário,
    # pois nesse momento, ele tanto é o que mais recebe, quanto o
    # que menos recebe.
    if not funcionario_mais_recebe:
        funcionario_mais_recebe.append(funcionario.copy())
    else:
        # caso contrário já vamos verificar se o salário é maior do que o que é maior atualmente
        # lembrem-se, estamos dentro de um loop
        if salario > funcionario_mais_recebe[0]['salario']:  # a verificação é sempre feita pelo primeiro elemento
            funcionario_mais_recebe = []  # limpa todos os funcionários, pois agora temos um novo que mais recebe
            funcionario_mais_recebe.append(funcionario.copy())
        elif salario == funcionario_mais_recebe[0]['salario']:
            funcionario_mais_recebe.append(funcionario.copy())  # se o salario for o mesmo, apenas adicionamos ele na lista

    if not funcionario_menos_recebe:
        funcionario_menos_recebe.append(funcionario.copy())
    else:
        if salario < funcionario_menos_recebe[0]['salario']:
            funcionario_menos_recebe = []
            funcionario_menos_recebe.append(funcionario.copy())
        elif salario == funcionario_menos_recebe[0]['salario']:
            funcionario_menos_recebe.append(funcionario.copy())

    area_codigo = funcionario['area']

    if not area_codigo in areas:
        areas[area_codigo] = {'codigo': area_codigo}

    area = areas[area_codigo]

    if area_codigo not in funcionario_area_mais_recebe:
        funcionario_area_mais_recebe[area_codigo] = []
        funcionario_area_mais_recebe[area_codigo].append(funcionario.copy())
    else:
        if salario > funcionario_area_mais_recebe[area_codigo][0]['salario']:
            funcionario_area_mais_recebe[area_codigo] = []
            funcionario_area_mais_recebe[area_codigo].append(funcionario.copy())
        elif salario == funcionario_area_mais_recebe[area_codigo][0]['salario']:
            funcionario_area_mais_recebe[area_codigo].append(funcionario.copy())

    if area_codigo not in funcionario_area_menos_recebe:
        funcionario_area_menos_recebe[area_codigo] = []
        funcionario_area_menos_recebe[area_codigo].append(funcionario.copy())
    else:
        if salario < funcionario_area_menos_recebe[area_codigo][0]['salario']:
            funcionario_area_menos_recebe[area_codigo] = []
            funcionario_area_menos_recebe[area_codigo].append(funcionario.copy())
        elif salario == funcionario_area_menos_recebe[area_codigo][0]['salario']:
            funcionario_area_menos_recebe[area_codigo].append(funcionario.copy())

    # inicializa o controle de soma dos funcionários para esse código da área
    if not area_codigo in area_funcionarios_soma:
        area_funcionarios_soma[area_codigo] = 0
    else:
        area_funcionarios_soma[area_codigo] += 1
        
    if not area_mais_funcionarios:
        area_mais_funcionarios = [area.copy()]
    else:
        if area_funcionarios_soma[area_codigo] > area_funcionarios_soma[area_mais_funcionarios[0]['codigo']]:
            area_mais_funcionarios = [area.copy()]
        elif area_funcionarios_soma[area_codigo] == area_funcionarios_soma[area_mais_funcionarios[0]['codigo']]:
            if not area in area_mais_funcionarios:
                area_mais_funcionarios.append(area.copy())
    if not area_menos_funcionarios:
        area_menos_funcionarios = [area.copy()]
    else:
        if area_funcionarios_soma[area_codigo] < area_funcionarios_soma[area_menos_funcionarios[0]['codigo']]:
            area_menos_funcionarios = [area.copy()]
        elif area_funcionarios_soma[area_codigo] == area_funcionarios_soma[area_menos_funcionarios[0]['codigo']]:
            if not area in area_menos_funcionarios:
                area_menos_funcionarios.append(area.copy())

    # antes de adicionar o sobrenome no controle é preciso verificar se já existe
    sobrenome = funcionario['sobrenome']
    if not sobrenome in sobrenome_mais_recebe:
        sobrenome_mais_recebe[sobrenome] = [funcionario.copy()]
    else:
        if salario > sobrenome_mais_recebe[sobrenome][0]['salario']:
            sobrenome_mais_recebe[sobrenome] = [funcionario.copy()]
        elif salario == sobrenome_mais_recebe[sobrenome][0]['salario']:
            sobrenome_mais_recebe[sobrenome].append(funcionario.copy())
    if sobrenome in sobrenome_controle:
        if not sobrenome in sobrenome_controle_duplicados:
            sobrenome_controle_duplicados.append(sobrenome)
    else:
        # se não existe o sobrenome ainda na lista, adiciona
        sobrenome_controle.append(sobrenome)

    # faz as somas
    funcionario_soma_receita += salario
    if not area_codigo in funcionario_area_soma_receita:
        funcionario_area_soma_receita[area_codigo] = salario
        funcionario_area_conta[area_codigo] = 1
    else:
        funcionario_area_soma_receita[area_codigo] += salario
        funcionario_area_conta[area_codigo] += 1

    # reinicia a variável funcionario
    funcionario_conta += 1
    funcionario = {}
    
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 
funcionario_media_receita = funcionario_soma_receita / funcionario_conta
for funcionario in funcionario_mais_recebe:
    print(u"global_max|%s %s|%.2f" % (funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))

for funcionario in funcionario_menos_recebe:
    print(u"global_min|%s %s|%.2f" % (funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))
print(u"global_avg|%.2f" % funcionario_media_receita)

for area_codigo, area in funcionario_area_mais_recebe.items():
    for funcionario in area:
        print(u"area_max|%s|%s %s|%.2f" % (areas[area_codigo]['nome'], funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))
for area_codigo, area in funcionario_area_menos_recebe.items():
    for funcionario in area:
        print(u"area_min|%s|%s %s|%.2f" % (areas[area_codigo]['nome'], funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))
for area_codigo, area in areas.items():
    try:
        media = funcionario_area_soma_receita[area_codigo] / funcionario_area_conta[area_codigo]
        print(u"area_avg|%s|%.2f" % (areas[area_codigo]['nome'], media))
    except KeyError:
        pass

for funcionario in area_mais_funcionarios:
    print(u"most_employees|%s|%d" % (funcionario['nome'], area_funcionarios_soma[funcionario['codigo']]))
for funcionario in area_menos_funcionarios:
    print(u"least_employees|%s|%d" % (funcionario['nome'], area_funcionarios_soma[funcionario['codigo']]))
for sobrenome in sobrenome_controle_duplicados:
    funcionarios = sobrenome_mais_recebe[sobrenome]
    for funcionario in funcionarios:
        print(u"last_name_max|%s|%s %s|%.2f" % (sobrenome, funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))
