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

# abre o arquivo json
file_name = 'funcionarios-10k.json'
arquivo = open(file_name)
file_size = os.path.getsize(file_name)
# Aqui declaramos todas as variáveis que utilizaremos para armazenar os resultados desejados
# é interessante que o nome da variável seja bem descritivo, mesmo sendo maior.

# os funcionários que mais recebem e os que menos recebem, e a média salarial da empresa
# para calcular a média precisaremos da quantidade de funcionários (len(funcionarios))
# e a soma
funcionario_conta = 0
funcionario_mais_recebe = None
funcionario_menos_recebe = None
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
#for json_areas in ijson.items(arquivo, 'areas'):
#    for area in json_areas:
#        areas[area['codigo']] = area

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
        funcionario_mais_recebe = funcionario.copy()
    else:
        # caso contrário já vamos verificar se o salário é maior do que o que é maior atualmente
        # lembrem-se, estamos dentro de um loop
        if salario > funcionario_mais_recebe['salario']:
            funcionario_mais_recebe = funcionario.copy()

    if not funcionario_menos_recebe:
        funcionario_menos_recebe = funcionario.copy()
    else:
        if salario < funcionario_menos_recebe['salario']:
            funcionario_menos_recebe = funcionario.copy()

    area_codigo = funcionario['area']

    if not area_codigo in areas:
        areas[area_codigo] = {'codigo': area_codigo}

    area = areas[area_codigo]

    if area_codigo not in funcionario_area_mais_recebe:
        funcionario_area_mais_recebe[area_codigo] = funcionario.copy()
    else:
        if salario > funcionario_area_mais_recebe[area_codigo]['salario']:
            funcionario_area_mais_recebe[area_codigo] = funcionario.copy()

    if area_codigo not in funcionario_area_menos_recebe:
        funcionario_area_menos_recebe[area_codigo] = funcionario.copy()
    else:
        if salario < funcionario_area_menos_recebe[area_codigo]['salario']:
            funcionario_area_menos_recebe[area_codigo] = funcionario.copy()

    # inicializa o controle de soma dos funcionários para esse código da área
    if not area_codigo in area_funcionarios_soma:
        area_funcionarios_soma[area_codigo] = 0
    else:
        area_funcionarios_soma[area_codigo] += 1
        
    if not area_mais_funcionarios:
        area_mais_funcionarios = area.copy()
    else:
        if area_funcionarios_soma[area_codigo] > area_funcionarios_soma[area_mais_funcionarios['codigo']]:
            area_mais_funcionarios = area.copy()
    if not area_menos_funcionarios:
        area_menos_funcionarios = area.copy()
    else:
        if area_funcionarios_soma[area_codigo] < area_funcionarios_soma[area_mais_funcionarios['codigo']]:
            area_mais_funcionarios = area.copy()

    # antes de adicionar o sobrenome no controle é preciso verificar se já existe
    sobrenome = funcionario['sobrenome']
    if not sobrenome in sobrenome_mais_recebe:
        sobrenome_mais_recebe[sobrenome] = funcionario.copy()
    else:
        if salario > sobrenome_mais_recebe[sobrenome]['salario']:
            sobrenome_mais_recebe[sobrenome] = funcionario.copy()
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
    

funcionario_media_receita = funcionario_soma_receita / funcionario_conta

funcionario = funcionario_mais_recebe
print(u"O Funcionario que mais recebe é %s %s, de ID %s com o salário de %d" % (funcionario['nome'], funcionario['sobrenome'], funcionario['id'], funcionario['salario']))
funcionario = funcionario_menos_recebe
print(u"O Funcionario que menos recebe é %s %s, de ID %s com o salário de %d" % (funcionario['nome'], funcionario['sobrenome'], funcionario['id'], funcionario['salario']))
print(u'A Média de Salário da empresa é de %d' % funcionario_media_receita)
for area_codigo, area in funcionario_area_mais_recebe.items():
    print(u'\nNa área %s, %s %s é o funcionário que MAIS recebe, com um salário de %d' % (areas[area_codigo]['nome'], area['nome'], area['sobrenome'], area['salario']))
    area_menos = funcionario_area_menos_recebe[area_codigo]
    print(u'O que MENOS recebe é o funcionário %s %s, com um salário de %d' % (area_menos['nome'], area_menos['sobrenome'], area_menos['salario']))
    media = funcionario_area_soma_receita[area_codigo] / funcionario_area_conta[area_codigo]
    print(u'E a média salarial nessa área é de %d\n' % media)

print(u'A área com mais funcionários é %s' % area_mais_funcionarios['nome'])
print(u'A área com menos funcionários é %s' % area_menos_funcionarios['nome'])
print('')
for sobrenome in sobrenome_controle_duplicados:
    funcionario = sobrenome_mais_recebe[sobrenome]
    print(u"De sobrenome %s, o funcionário que mais recebe é %s %s, com um salário de %d" % (sobrenome, funcionario['nome'], funcionario['sobrenome'], funcionario['salario']))