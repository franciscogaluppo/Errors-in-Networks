import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import tkinter

def bfs(g, lista, centro, vertice, distMax, distAtual):
	if (distAtual > distMax):
		return
	for i in g.neighbors(vertice):
		if distAtual < g.node[i]["distancia"]:
			g.node[i]["distancia"] = distAtual
			g.node[i]["comunidade"] = centro
			if i in lista:
				lista.remove(i)
			bfs(g, lista, centro, i, distMax, distAtual + 1)



arq = "set1.txt"
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()
lista = [] #lista que contem os vertices que nao estao em nenhuma comunidade


for i in range(N):
	g.node[i]["distancia"] = 1000
	g.node[i]["comunidade"] = -1
	lista.append(i + 1)

quantidade = 0

while len(lista) > 2:
	#escolhe um vertice aleatorio
	centro = lista[rd.randrange(0, len(lista) - 1)]


	if g.node[centro]["comunidade"] == -1:  #se ele nao estiver em nenhuma comunidade, cria uma comunidade para ele
		g.node[centro]["distancia"] = 0
		g.node[centro]["comunidade"] = centro
		lista.remove(centro)
		bfs(g, lista, centro, centro, 2, 1)
		quantidade += 1



print ("Total de comunidades: {}".format(quantidade))

nx.draw_networkx(g)
plt.show()
