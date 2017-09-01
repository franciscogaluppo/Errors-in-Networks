import networkx as nx
import random

def a(valor):
	if valor <= 0:
		return 0
	return 1

def numero(grafo, vertice, Z):
	tratamento = 0
	for i in nx.all_neighbors(grafo, vertice):
		tratamento += Z[i]

	return tratamento

def init(arq, alpha, beta, gama, kappa, cent):
	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()

	#Cria um vetor Z de tamanho N com os tratamentos
	Z = []
	for i in range (N):
		if random.random() < (cent/100):
			Z.append(0)
		else:
			Z.append(1)
	#Cria um vetor U de tamanho N com os componentes estocasticos
	U = []
	for i in range(N):
		U.append(random.normalvariate(0, 0.05))
	#Cria um vetor Y que tera os resultados e tamanho N
	Y = []


	#Variaveis para definir os resultados
	NumDeUns = 0
	NumDeUnsComZ0 = 0
	NumDeZ0 = 0


	for i in range(N):
		if Z[i] == 0 and numero(g, i, Z) < kappa:    #grupo de controle
			Y.append(a(alpha + U[i]))
		elif Z[i] == 1 and numero(g, i, Z) > kappa:  #grupo de tratamento
			Y.append((alpha + beta + U[i]))
		else:                                        #sobra
			Y.append(a(alpha +(Z[i]*gama + (1 - gama)*min(kappa, numero(g, i, Z))*beta/(gama + (1 - gama)*kappa) + U[i])))

		if Y[i] == 1:
			NumDeUns += 1
			if Z[i] == 0:
				NumDeUnsComZ0 += 1

		if Z[i] == 0:
			NumDeZ0 += 1

	print("\n--Número")
	print("Fração de nós com Yi = 1: {}".format(NumDeUns/N))
	try:
		print("Fração de nós com Yi = 1 dado que Z = 0: {0}".format(NumDeUnsComZ0/NumDeZ0))
	except ZeroDivisionError:
		print("Não há nós com Z=0")
	print("Fração de nós com Yi = 1 dado que Z = 1: {}".format((NumDeUns - NumDeUnsComZ0)/(N - NumDeZ0)))
