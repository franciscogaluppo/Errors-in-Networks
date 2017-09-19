import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import tkinter

def bfs(g, lista, centro, vertice, distMax, distAtual, comunidades, indice):
	if (distAtual > distMax):
		return
	for i in g.neighbors(vertice):
		if distAtual < g.node[i]["distancia"]:
			g.node[i]["distancia"] = distAtual
			g.node[i]["comunidade"] = centro
			lista[indice].append(i)
			#print("  Na comunidade {} o vertice {} tem distancia {} e e vizinho de {}".format(centro, i, distAtual, vertice))
			if i in lista:
				lista.remove(i)
			bfs(g, lista, centro, i, distMax, distAtual + 1)



arq = "set3.txt"
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()
lista = [] #lista que contem os vertices que nao estao em nenhuma comunidade
comunidades = []
indice = 0



for i in range(N):
	#print(i)
	g.node[i]["distancia"] = 1000
	g.node[i]["comunidade"] = -1
	lista.append(i + 1)

quantidade = 0

while len(lista) > 2:
	#escolhe um vertice aleatorio
	centro = lista[rd.randrange(0, len(lista) - 1)]

	#print("Centro: {}".format(centro))

	if g.node[centro]["comunidade"] == -1:  #se ele nao estiver em nenhuma comunidade, cria uma comunidade para ele
		g.node[centro]["distancia"] = 0
		g.node[centro]["comunidade"] = centro
		lista.remove(centro)
		comunidades.append([centro])
		bfs(g, lista, centro, centro, 50, 1, comunidades, indice)
		print("Comunidade: {}".format(centro))
		quantidade += 1



print ("Total: {}".format(quantidade))

nx.draw_networkx(g)
plt.draw()
