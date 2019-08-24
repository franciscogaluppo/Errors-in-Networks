from os import system

from Funcs import Simulate
from Funcs import Estimate
from Funcs import Sugar
from Funcs import IO

import matplotlib.pyplot as plt
import numpy as np

nome = "Wiki-Vote"
g = Sugar.get_graph(Sugar.path(nome))
nodes = g.number_of_nodes()

p = 1
q = 1

<<<<<<< HEAD
ins = [False, 0.95, True]
cores = ['r', 'b', 'g', 'y', 'm']
=======
ins = [False, 0.5, True]
cores = ['r', 'b', 'g', 'y', 'm', 'k']
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf

betas = [[0, 0, 1],
		[0, 0.5, 0.5],
		[0, 1, 0],
		[0, 1, 1],
		[0, 1, 2]]

modelos =  ["SUTVA",
			"Linear",
<<<<<<< HEAD
			"Médias C1 C0"]
=======
			"Probit",
			"Logistic",
			"Médias C1 C0",
			"Linear C1 C0"]
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf

print("Processo inicializado")
conjunto_da_obra = []

# Gera o tratamento
system("g++ Clusterização/FENNEL_ZVEC.cpp -o CLST.PRGM")
<<<<<<< HEAD
system("./CLST.PRGM {} {} {} {} {} {} {} {} {}".format(nome, nodes, 10, 1, 10, 1010, 10, p, q))
system("rm -f CLST.PRGM")
print("Clusters prontos\nInicialiando as simulações")

for clusters in range(10, 1010, 10):
=======
system("./CLST.PRGM {} {} {} {} {} {} {}".format(nome, nodes, 10, 0.0001, 100, 1100, 100, p, q))
system("rm -f CLST.PRGM")
print("Clusters prontos\nInicialiando as simulações")

for clusters in range(100, 1100, 100):
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf
	# Leitura do tratamento
	zvec = np.empty(shape=(nodes))
	path = "Datasets/{}/real-{}.txt".format(nome, clusters)
	tf = open(path, "r")
	j = 0
	for i in tf:
		zvec[j] = int(i[0])
		j += 1
	tf.close()

	# Gera os dados
<<<<<<< HEAD
	vals = Estimate.multiple_estimate(g, zvec, ins, betas, 3, [1, 2, 5], 10, "Tau-Exposure", [0, 1], True)
	IO.write_results(vals[1], vals[0], betas, modelos,
		"Real/", nome + " {} {}|{}".format(clusters, p, q))
=======
	vals = Estimate.multiple_estimate(g, zvec, ins, betas, runs=50, tau_param=0.5)
	IO.write_results(vals[0], vals[1], betas, modelos,
		"Resultados/Valores Teste Tau-Exposure/",
		nome + " {} {}|{}".format(clusters, p, q))
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf
	conjunto_da_obra.append(vals)

	system("rm -f {}".format(path))

	# Porcentagem do limite
	print("{} %".format(clusters*100/(1010-10)))

valores = np.array(conjunto_da_obra)

print("Criando os gráficos")
# Gráfico MSE x Número de clusters
<<<<<<< HEAD
x = np.array([i for i in range(10, 1010, 10)])
=======
x = np.array([x for x in range(100, 1100, 100)])
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf

plt.rc('axes', titlesize=6)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

xtick = []
ytick = []

f, axarr = plt.subplots(len(modelos), len(betas), sharex='col', sharey='row')
for i in range(len(modelos)):
	for j in range(len(betas)):
		y = [((valores[x][0][i][j] - valores[x][1][i][j])**2).mean() for x in range(100)]
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
<<<<<<< HEAD
plt.savefig("Gráfico Real.png", dpi=100)
=======
plt.savefig("Gráfico #2.png", dpi=100)
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf
print("Processo terminado")
