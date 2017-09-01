# Módulos
from random import random as rd
import numpy as np
import networkx as nx


# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Entradas
arq = input("Arquivo: ")
alpha = float(input("Alpha: "))
beta = float(input("Beta: "))
gama = float(input("Gama: "))
cent = int(input("%z=0: "))
T = int(input("T: "))


# Declarações
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()
A = nx.to_numpy_matrix(g)
z1 = 0


# cent% da população recebe o tratamento z=0 e o restante o z=1
# A resposta inicial de ambos é y=0
for i in range(N):
	if rd() < cent/100:
		g.node[i]['y'] = 0
		g.node[i]['z'] = 0
	else:
		g.node[i]['y'] = 0
		g.node[i]['z'] = 1
		z1 += 1


# Vetor auxiliar para armazenar os valores atuais
Y = np.zeros(N)

# Tempo discreto
for i in range(T):

	# Componente estocástico
	U = np.random.normal(0, 1, N)

	# Aplica a função ao grafo
	for j in range(N):
		
		# Soma dos tratamentos dos nós vizinhos de j
		soma = 0
		for k in g.neighbors(j): soma += g.node[k]['y']

		# Aplica a função ao nó j
		Y[j] = a(alpha + (beta * g.node[j]['z']) + (gama * soma/ g.degree(j)) + U[j])

	# Atualiza as respostas dos nós com os novos valores
	for j in range(N):
		g.node[j]['y'] = Y[j]


# Resultados
y1 = 0
y1z1 = 0


# Contagem
for i in range(N):
	if g.node[i]['y'] == 1:
		y1 += 1
		if g.node[i]['z'] == 1:
			y1z1 += 1


# Imprime os resultados
print("\nFração de nós com Yi=1: {}".format(y1 / N))

if N - z1 != 0:
	print("Fração de nós com Yi=1 dado que Z=0: {}".format((y1 - y1z1) / (N - z1)))
else:
	print("Não há nós com Yi=0")

if z1 != 0:
	print("Fração de nós com Yi=1 dado que Z=1: {}".format(y1z1 / z1))
else:
	print("Não há nós com Yi=1")