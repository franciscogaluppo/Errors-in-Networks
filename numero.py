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

arq = raw_input("Arquivo: ")
alpha = float(input("Alpha: "))
beta = float(input("Beta: "))
gama = float(input("Gama: "))
kappa = float(input("Kappa: "))

g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()

#Cria um vetor Z de tamanho N com os tratamentos
Z = []
for i in range (N):
	if random.random() < 0.1: #esse valor pode ser alterado para mudar a quantidade de pessoas com tratamento
		Z.append(0)
	else:
		Z.append(1)
#Cria um vetor U de tamanho N com os componentes estocasticos
U = []
for i in range(N):
	U.append(random.random())
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

print "Fracao de nos com Yi = 1: {}".format(NumDeUns/N)
print "Fracao de nos com Yi = 1 dado que Z = 0: {}".format(NumDeUnsComZ0/NumDeZ0)
print "Fracao de nos com Yi = 1 dado que Z = 1: {}".format((NumDeUns - NumDeUnsComZ0)/(N - NumDeZ0))