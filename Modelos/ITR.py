import numpy as np
import networkx as nx

from funcs import a
from funcs import comunidade as com

# Função ITR
def itr(g, ins, zvector, comu=-1):

	# Entradas
	alpha = ins[0]
	ite = ins[1]

	if comu != -1:
		membros = com(comu)	

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	for i in range(ite):

		# Componente Estocástico
		U = np.random.normal(0, 1, N)
		if comu != -1:
			for k in membros:
				U[k] = np.random.normal(0.5, 0.8)

		# Aplica a função ao grafo
		for j in range(N):
			g.node[j]['y'] = a(alpha * g.node[j]['z'] + U[j])
			
	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])
		
	return(yvector)