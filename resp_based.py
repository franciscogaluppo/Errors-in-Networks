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
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()
A = nx.to_numpy_matrix(g)

# Vetores com Tratamento = 1 e com Tratamento = 0
Y1 = np.zeros(N)
Y0 = np.zeros(N)

# Tempo discreto
for i in range(ite):
	X1 = Y1
	U1 = np.random.normal(0, 1, N)

	X0 = Y0
	U2 = np.random.normal(0, 1, N)

	# Aplica o Tratamento 1 e 0 para todo nó
	for j in range(N):
		Y1[j] = a(alpha + beta + (gama * np.asscalar(np.dot(X1, A[j].transpose())) / g.degree(j)) + U1[j])
		Y0[j] = a(alpha + (gama * np.asscalar(np.dot(X0, A[j].transpose())) / g.degree(j)) + U2[j])

# Imprime a média entre os tratamentos
print("Média:", (sum(Y1) - sum(Y0)) / N)