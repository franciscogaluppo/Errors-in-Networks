import numpy as np
import networkx as nx

#from funcs import comunidade as com

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função Response Based
def resp(g, ins, zvector, comu=None):

	# Entradas
	alpha = ins[0]
	beta = ins[1]
	gama = ins[2]
	T = ins[3]

	if comu != None:
		membros = com(comu)	

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]
		g.node[i]['y'] = 0

	# Componente estocástico
	U = np.random.normal(ins[4], ins[5], N)

	if comu != None:
		for k in membros:
			U[k] = np.random.normal(0.5, 0.8)

	for i in range(T):

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

	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])
		
	return(yvector)