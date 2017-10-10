import numpy as np
import networkx as nx

from comu import comunidade as com

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função ITR
def itr(g, ins, zvector, comu=None):

	# Entradas
	alpha = ins[0]

	if comu != None:
		membros = com(comu)	

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	# Componente Estocástico
	U = np.random.normal(ins[1], ins[2], N)
	if comu != None:
		for k in membros:
			U[k] = np.random.normal(0.5, 0.8)

	# Aplica a função ao grafo
	for j in range(N):
		g.node[j]['y'] = a(alpha * g.node[j]['z'] + U[j])
			
	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])
		
	return(yvector)