# Método mais simples

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
ite = int(input("Iterações: "))

# Declarações
results = []
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()

# Laço
for j in range(ite):
	out = 0

	# Componente Estocástico
	U = np.random.normal(0, 1, N)

	# ((Somatório do tratamento 1) - (Somatório do tratamento 0)) / N
	for i in range(N):
		out += a(U[i] + alpha) - a(U[i])
	results.append(out / N)

print("\nMédia: {}\nVariância: {}".format(np.median(results), np.var(results)))	
	