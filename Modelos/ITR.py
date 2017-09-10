# Módulos
from random import random as rd
import networkx as nx
from funcs import a
import numpy as np

# Função ITR
def itr(ins, trat=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	ite = ins[2]

	# Lista dos resultados
	res = [0,0,0]

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


	# Laço
	for i in range(ite):

		# Componente Estocástico
		U = np.random.normal(0, 1, N)

		# Pessoas com y=1 e pessoas com y=1 e z=1
		y1 = 0
		y1z1 = 0

		# Aplica a função ao grafo
		for j in range(N):
			
			# Aplica a função ao nó j
			g.node[j]['y'] = a(alpha * g.node[j]['z'] + U[j])
			
			# Contagem
			if g.node[j]['y'] == 1:
				y1 += 1
				if g.node[j]['z'] == 1:
					y1z1 += 1

		# Passa os valores para as listas de resultado
		res[0] += y1/N
		if N - z1 != 0:
			res[1] += (y1 - y1z1) / (N - z1)
		if z1 != 0:
			res[2] += y1z1 / z1





	# Retorno
	out = [res[0]/ite, -1, -1]

	if z1 != N:
		out[1] = res[1]/ite

	if z1 != 0:
		out[2] = res[2]/ite

	return(out)