# Módulos
from random import random as rd
import networkx as nx
from funcs1 import a
from funcs1 import comunidade as com
import numpy as np


# Função Fração
def frac(ins, trat=-1, comu=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	tau = ins[4]

	if comu != -1:
		membros = com(comu)	

	# Declarações
	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()
	z1 = 0


	# Caso não haja tratamento, porcentagem é o padrão
	if trat == -1:

		# Entrada da porcentagem
		cent = float(input("%z=0: "))

		# cent% da população recebe o tratamento z=0 e o restante o z=1
		for i in range(N):
			if rd() < cent/100:
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
		frac = soma / g.degree(i)

		#
		if g.node[i]['z'] == 0 and frac < tau:
			g.node[i]['y'] = a(alpha + U[i])

		#
		elif g.node[i]['z'] == 1 and frac > tau:
			g.node[i]['y'] = a(alpha + beta + U[i])

		#
		else:
			g.node[i]['y'] = a(alpha + beta*(frac*(1 - gama) + g.node[i]['z']*gama) + U[i])

		# Contagem
		if g.node[i]['y'] == 1:
			y1 += 1
			if g.node[i]['z'] == 1:
				y1z1 += 1

	# Retorno
	out = [y1 / N, -1, -1, N]

	if z1 != N:
		out[1] = (y1 - y1z1) / (N - z1)

	if z1 != 0:
		out[2] = (y1z1 / z1)

	return(out)