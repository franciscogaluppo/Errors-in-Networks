import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from Modelos.resp_based import resp

alpha = np.sort(np.random.normal(0, 1, 10))
beta = np.sort(np.random.normal(0, 1, 10))
gama = np.sort(np.random.normal(0, 1, 10))

Y = []

for a in alpha:
	for b in beta:
		for g in gama:
			Y.append(resp(["set1.txt", a, b, g, 10], "zeta.txt")[0])

fig = plt.figure()
ax = fig.gca()

ax.set_xticks(np.arange(0, 1000, 100))
ax.set_yticks(np.arange(0, 1., 0.1))

plt.scatter(np.arange(0, 1000, 1), Y)
plt.grid()
plt.show()