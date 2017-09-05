# Módulos
from random import random as rd
import networkx as nx
from funcs import a
import numpy as np

# Função ITR
def itr(ins):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	cent = ins[2]
	ite = ins[3]

	# Listas dos resultados
	res1 = []
	res2 = []
	res3 = []

	# Declarações
	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()
	z1 = 0


	# cent% da população recebe o tratamento z=0 e o restante o z=1
	# A resposta inicial de ambos é y=0
	for i in range(N):
		if rd() < cent/100:
			g.node[i]['z'] = 0
		else:
			g.node[i]['z'] = 1
			z1 += 1


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
		res1.append(y1/N)
		if N - z1 != 0:
			res2.append((y1 - y1z1) / (N - z1))
		if z1 != 0:
			res3.append(y1z1 / z1)

	# Retorno
	out = [np.mean(res1), np.std(res1)]

	if z1 != N:
		out.append(np.mean(res2))
		out.append(np.std(res2))
	else:
		out.append(-1)
		out.append(-1)

	if z1 != 0:
		out.append(np.mean(res3))
		out.append(np.std(res3))
	else:
		out.append(-1)
		out.append(-1)

	return(out)