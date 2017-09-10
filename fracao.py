import networkx as nx
from funcs import a
import random

def fracao(grafo, vertice, Z):
	tratamento = 0
	for i in nx.all_neighbors(grafo, vertice):
		tratamento += Z[i]

	return tratamento/grafo.degree(vertice)


def init(ins, trat=-1):

	# Entradas
	arq = ins[0]
	alpha = ins[1]
	beta = ins[2]
	gama = ins[3]
	tau = ins[4]

	g = nx.read_edgelist(arq, nodetype=int)
	N = g.number_of_nodes()

	#Cria um vetor Z de tamanho N com os tratamentos
	Z = []

	# Caso não haja tratamento, porcentagem é o padrão
	if trat == -1:

		# Entrada da porcentagem
		cent = float(input("%z=0: "))

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
		if Z[i] == 0 and fracao(g, i, Z) < tau:
			Y.append(a(alpha + U[i]))
		elif Z[i] == 1 and fracao(g, i, Z) > tau:
			Y.append(a(alpha + beta + U[i]))
		else:
			Y.append(a(alpha + beta*(fracao(g, i, Z)*(1 - gama) + Z[i]*gama) + U[i]))

		if Y[i] == 1:
			NumDeUns += 1
			if Z[i] == 0:
				NumDeUnsComZ0 += 1

		if Z[i] == 0:
			NumDeZ0 += 1

	# Retorno
	out = [NumDeUns/N, -1, -1]

	if NumDeZ0 != 0:
		out[1] = NumDeUnsComZ0/NumDeZ0

	if NumDeZ0 != N:
		out[2] = (NumDeUns - NumDeUnsComZ0)/(N - NumDeZ0)

	return(out)