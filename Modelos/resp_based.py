# Módulos
from random import random as rd
import networkx as nx
from funcs1 import a
from funcs1 import comunidade as com
import numpy as np


# Função Response Based
def resp(ins, trat=-1, comu=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	T = ins[4]

	if comu != -1:
		membros = com(comu)	

	# Declarações
	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()
	A = nx.to_numpy_matrix(g)
	z1 = 0


	# Caso não haja tratamento, porcentagem é o padrão
	if trat == -1:

		# Entrada da porcentagem
		cent = float(input("%z=0: "))

		# cent% da população recebe o tratamento z=0 e o restante o z=1
		# A resposta inicial de ambos é y=0
		for i in range(N):
			if rd() < cent/100:
				g.node[i]['y'] = 0
				g.node[i]['z'] = 0
			else:
				g.node[i]['y'] = 0
				g.node[i]['z'] = 1
				z1 += 1

	# Caso haja tratamento
	else:
		tf = open(trat, "r")

		for i in range(N):
			r = tf.readline()
			g.node[i]['y'] = 0
			g.node[i]['z'] = int(r[0])
			if int(r[0]) == 1:
				z1 += 1
		tf.close()


	# Tempo discreto
	for i in range(T):

		# Componente estocástico
		U = np.random.normal(0, 1, N)
		if comu != -1:
			for k in range(N):
				if k in membros:
					U[k] = np.random.normal(0.5, 0.8)

		# Aplica a função ao grafo
		for j in range(N):
			
			# Soma dos tratamentos dos nós vizinhos de j
			soma = 0
			for k in g.neighbors(j): soma += g.node[k]['y']

			# Aplica a função ao nó j
			g.node[j]["y'"] = a(alpha + (beta * g.node[j]['z']) + (gama * soma/ g.degree(j)) + U[j])

		# Atualiza as respostas dos nós com os novos valores
		for j in range(N):
			g.node[j]['y'] = g.node[j]["y'"]


	# Resultados
	y1 = 0
	y1z1 = 0


	# Contagem
	for i in range(N):
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
