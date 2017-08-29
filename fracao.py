import random

def a(valor):
	if valor <= 0:
		return 0
	return 1

def fracao(grafo, vertice, Z):
	tratamento = 0
	for i in nx.all_neighbors(grafo, vertice):
		tratamento += Z[i]

	return tratamento/grafo.degree(i)

arq = raw_input("Arquivo: ")
alpha = float(input("Alpha: "))
beta = float(input("Beta: "))
gama = float(input("Gama: "))
tau = float(input("Tau: "))
porcentagem = float(input("Porcentagem: "))

g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()

#Cria um vetor Z de tamanho N com os tratamentos
Z = []
for i in range (N):
	if random.random() < (porcentagem/100):
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
		Y.append((alpha + beta + U[i]))
	else:
		Y.append(a(alpha + beta*(fracao(g, i, Z)*(1 - gama) + Z[i]*gama) + U[i]))

	if Y[i] == 1:
		NumDeUns += 1
		if Z[i] == 0:
			NumDeUnsComZ0 += 1

	if Z[i] == 0:
		NumDeZ0 += 1

print ("Fracao de nos com Yi = 1: {0}".format(NumDeUns/N))
try:
    print ("Fracao de nos com Yi = 1 dado que Z = 0: {0}".format(NumDeUnsComZ0/NumDeZ0))
except ZeroDivisionError:
    print ("Nao e possivel exibir Yi = 1 dado que Z = 0")
print ("Fracao de nos com Yi = 1 dado que Z = 1: {0}".format((NumDeUns - NumDeUnsComZ0)/(N - NumDeZ0)))
