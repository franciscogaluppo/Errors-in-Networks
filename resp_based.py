# Método mais robusto

# Módulos
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
ite = int(input("Iterações: "))

# Declarações
results = []
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()
Y1 = np.zeros(N)
Y0 = np.zeros(N)

for i in range(ite):
	X1 = Y1
	U1 = np.random.normal(0, 1, N)

	X0 = Y0
	U2 = np.random.normal(0, 1, N)

	for j in range(N):
		Y1[j] = a(alpha + beta + (gama * np.asscalar(np.dot(X1, nx.to_numpy_matrix(g)[j].transpose())) / N) + U1[j])
		Y0[j] = a(alpha + (gama * np.asscalar(np.dot(X0, nx.to_numpy_matrix(g)[j].transpose())) / N) + U2[j])