# Cria o arquivo teste de entrada

import networkx as nx

g = nx.read_edgelist("set1.txt", nodetype=int)
N = g.number_of_nodes()

arq = open("zeta.txt", "w")
for i in range(N):
	if i % 2 == 0:
		arq.write("0\n")
	else:
		arq.write("1\n")