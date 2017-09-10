import networkx as nx
from random import random as rd
from funcs import a


def fracao(grafo, vertice):
	tratamento = 0
	for i in nx.all_neighbors(grafo, vertice):
		tratamento += grafo.node[i]['z']

	return tratamento/grafo.degree(vertice)


def init(ins, trat=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	tau = ins[4]
	cent = int(input("%z=0: "))

	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()


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

	#Cria um vetor U de tamanho N com os componentes estocasticos
	U = []
	for i in range(N):
		U.append(rd())
	#Cria um vetor Y que tera os resultados e tamanho N
	Y = []


	#Variaveis para definir os resultados
	NumDeUns = 0
	NumDeUnsComZ0 = 0
	NumDeZ0 = 0


	for i in range(N):
		if g.node[i]['z'] == 0 and fracao(g, i) < tau:
			Y.append(a(alpha + U[i]))
		elif g.node[i]['z'] == 1 and fracao(g, i) > tau:
			Y.append(a(alpha + beta + U[i]))
		else:
			Y.append(a(alpha + beta*(fracao(g, i)*(1 - gama) + g.node[i]['z']*gama) + U[i]))

		if Y[i] == 1:
			NumDeUns += 1
			if g.node[i]['z'] == 0:
				NumDeUnsComZ0 += 1

		if g.node[i]['z'] == 0:
			NumDeZ0 += 1

	# Retorno
	out = [NumDeUns/N, -1, -1]

	if NumDeZ0 != 0:
		out[1] = NumDeUnsComZ0/NumDeZ0

	if NumDeZ0 != N:
		out[2] = (NumDeUns - NumDeUnsComZ0)/(N - NumDeZ0)

	return(out)