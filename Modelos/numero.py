import networkx as nx
from random import random as rd
from funcs import a


def numero(grafo, vertice):
	tratamento = 0
	for i in nx.all_neighbors(grafo, vertice):
		tratamento += grafo.node[i]['z']

	return tratamento


def init(ins, trat=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	kappa = ins[4]
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
		if g.node[i]['z'] == 0 and numero(g, i) < kappa:    #grupo de controle
			Y.append(a(alpha + U[i]))
		elif g.node[i]['z'] == 1 and numero(g, i) > kappa:  #grupo de tratamento
			Y.append(a(alpha + beta + U[i]))
		else:                                        #sobra
			Y.append(a(alpha +(g.node[i]['z']*gama + (1 - gama)*min(kappa, numero(g, i))*beta/(gama + (1 - gama)*kappa) + U[i])))

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