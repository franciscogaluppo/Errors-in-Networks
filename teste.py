import functions as f
import networkx as nx

g = nx.read_edgelist("email-Eu-core.txt", nodetype=int)

f.plot(g)