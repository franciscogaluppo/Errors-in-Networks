#%%
import numpy as np
import functions as f
import networkx as nx

#%%
g = nx.read_edgelist("email-Eu-core.txt", nodetype=int)

f.plot(g)

#%%
print("Elementar")

#%%
s = np.random.normal(0, 1, g.number_of_nodes())
print(s)