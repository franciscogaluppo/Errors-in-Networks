import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist("email-Eu-core.txt", nodetype=int)

# print(g.degree())

nx.draw_networkx(g)
plt.show()