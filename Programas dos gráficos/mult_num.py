import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from Modelos.numero import num

alpha = np.sort(np.random.normal(0, 1, 10))
beta = np.sort(np.random.normal(0, 1, 10))
gama = np.sort(np.random.normal(0, 1, 10))
kappa = np.sort(np.random.normal(10, 4, 10))

Y = []

for a in alpha:
	for b in beta:
		for g in gama:
			for k in kappa:
				Y.append(num(["set1.txt", a, b, g, k], "zeta.txt")[0])

fig = plt.figure()
ax = fig.gca()

ax.set_xticks(np.arange(0, 10000, 1000))
ax.set_yticks(np.arange(0, 1., 0.1))

plt.scatter(np.arange(0, 10000, 1), Y)
plt.grid()
plt.show()