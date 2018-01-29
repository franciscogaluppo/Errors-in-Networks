from os import system

from Funcs import Simulate
from Funcs import Estimate
from Funcs import Sugar
from Funcs import IO

import matplotlib.pyplot as plt
import numpy as np

nome = "p2p-Gnutella08"
g = Sugar.get_graph(Sugar.path(nome))
nodes = g.number_of_nodes()

p = 1
q = 1

ins = [False, 0.5, True]
cores = ['r', 'b', 'g', 'y', 'm']

betas = [[0, 0, 1],
		[0, 0.5, 0.5],
		[0, 1, 0],
		[0, 1, 1],
		[0, 1, 2]]

modelos =  ["SUTVA",
			"Linear",
			"Probit",
			"Logistic",
			"Médias C1 C0"]

print("Processo inicializado")
conjunto_da_obra = []

# Gera o tratamento
system("g++ Clusterização/FENNEL_ZVEC.cpp -o CLST.PRGM")
system("./CLST.PRGM {} {} {} {} {} {} {} {} {}".format(nome, nodes, 10, 0.0001, 10, 110, 10, p, q))
system("rm -f CLST.PRGM")
print("Clusters prontos\nInicialiando as simulações")

for clusters in range(100, 1100, 100):
	# Leitura do tratamento
	zvec = np.empty(shape=(nodes))
	path = "Datasets/{}/comunidades-{}.txt".format(nome, clusters)
	tf = open(path, "r")
	j = 0
	for i in tf:
		zvec[j] = int(i[0])
		j += 1
	tf.close()

	print(sum(zvec)/len(zvec))

	# Gera os dados
	vals = Estimate.multiple_estimate(g, zvec, ins, betas, 3, [1, 2, 3, 4, 5], 10, [0, 1], True, 0.5)
	IO.write_results(vals[1], vals[0], betas, modelos,
		"Resultados/Valores Teste Tau-Exposure/",
		nome + " {} {}|{}".format(clusters, p, q))
	conjunto_da_obra.append(vals)

	system("rm -f {}".format(path))

	# Porcentagem do limite
	print("{} %".format(clusters*100/(1100-100)))

# valores = np.array(conjunto_da_obra)
valores = conjunto_da_obra

print("Criando os gráficos")
# Gráfico MSE x Número de clusters
x = np.array([x for x in range(100, 1100, 100)])

plt.rc('axes', titlesize=6)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

xtick = []
ytick = []

f, axarr = plt.subplots(len(modelos), len(betas), sharex='col', sharey='row')
for i in range(len(modelos)):
	for j in range(len(betas)):
		y = [((valores[x][0][i][j] - valores[x][1][i][j])**2).mean() for x in range(10)]
		axarr[i, j].plot(x, y, color=cores[i])
		axarr[i, j].set_title('{} {}'.format(modelos[i], betas[j]))

		if(i != len(modelos)-1):
			xtick.append(axarr[i, j])

		if(j != 0):
			ytick.append(axarr[i, j])

f.tight_layout()
#f.set_size_inches(18.5, 10.5, forward=True)

#plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
#plt.setp([a.get_xticklabels() for a in xtick], visible=False)
#plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
#plt.setp([a.get_yticklabels() for a in ytick], visible=False)

#plt.show()
plt.savefig("Gráfico #2.png", dpi=100)
print("Processo terminado")
