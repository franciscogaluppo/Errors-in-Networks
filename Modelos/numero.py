# Módulos
from random import random as rd
import networkx as nx
from funcs import a
from Comunidade import comunidade as com
import numpy as np


# Função Número
def num(ins, trat=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	kappa = ins[4]

	# Declarações
	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()
	z1 = 0


	# Caso não haja tratamento, porcentagem é o padrão
	if trat == -1:

		membros = [] #vetor que vai guardar quais vértices fazem parte da maior comunidade
		comu = str(input("Arquivo com comunidades(se não houver digite 0): "))
		if comu != "0":
			membros = com(comu)

		# Entrada da porcentagem
		cent = float(input("%z=0: "))

		# cent% da população recebe o tratamento z=0 e o restante o z=1
		for i in range(N):
			if i in membros: #se o vértice estiver na comunidade, ele recebe tratamento especial
				g.node[i]['z'] = np.random.normal(0.5, 0.8)
			elif rd() < cent/100:
				g.node[i]['z'] = 0
			else:
				g.node[i]['z'] = 1
				z1 += 1

	# Caso haja tratamento
	else:
		tf = open(trat, "r")

		for i in range(N):
			r = tf.readline()
			g.node[i]['z'] = int(r[0])
			if int(r[0]) == 1:
				z1 += 1
		tf.close()

	
	# Componente Estocástico
	U = np.random.normal(0, 1, N)

	# Pessoas com y=1 e pessoas com y=1 e z=1
	y1 = 0
	y1z1 = 0


	for i in range(N):

		# Soma dos tratamentos dos nós vizinhos de i
		soma = 0
		for k in g.neighbors(i): soma += g.node[k]['z']

		# Grupo de controle
		if g.node[i]['z'] == 0 and soma < kappa:
			g.node[i]['y'] = a(alpha + U[i])

		# Grupo de tratamento
		elif g.node[i]['z'] == 1 and soma > kappa:
			g.node[i]['y'] = a(alpha + beta + U[i])
		
		# Sobra
		else:
			g.node[i]['y'] = a(alpha + (g.node[i]['z']*gama + (1 - gama)*min(kappa, soma)*beta/(gama + (1 - gama)*kappa) + U[i]))

		# Contagem
		if g.node[i]['y'] == 1:
			y1 += 1
			if g.node[i]['z'] == 1:
				y1z1 += 1

	# Retorno
	out = [y1 / N, -1, -1]

	if z1 != N:
		out[1] = (y1 - y1z1) / (N - z1)

	if z1 != 0:
		out[2] = (y1z1 / z1)

	return(out)