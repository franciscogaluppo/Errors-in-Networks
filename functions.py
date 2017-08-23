import networkx as nx
import matplotlib.pyplot as plt

def a(valor):
	if valor <= 0: return 0
	return 1

def plot(graph):
	nx.draw_networkx(graph)
	plt.show()