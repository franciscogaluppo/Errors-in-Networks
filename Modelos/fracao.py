import numpy as np
import networkx as nx
from funcs import a
from funcs import comunidade as com

# Função Fração
def frac(g, ins, zvector, comu=None):

	# Entradas
	alpha = ins[0]
	beta = ins[1]
	gama = ins[2]
	linear = ins[3]
	tau = ins[4]

	if comu != None:
		membros = com(comu)	

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	# Componente Estocástico
	U = np.random.normal(ins[5], ins[6], N)

	if comu != None:
		for k in range(N):
			if k in membros:
				U[k] = np.random.normal(0.5, 0.8)


	for i in range(N):

		soma = 0
		for k in g.neighbors(i): soma += g.node[k]['z']
		frac = soma / g.degree(i)

		if g.node[i]['z'] == 0 and frac < tau and not linear:
			g.node[i]['y'] = a(alpha + U[i])

		elif g.node[i]['z'] == 1 and frac > tau and not linear:
			g.node[i]['y'] = a(alpha + beta + U[i])

		else:
			g.node[i]['y'] = (alpha + beta*g.node[i]['z'] + gama*frac + U[i])

	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])
		
	return(yvector)