import funcs as f
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = int(argv[1])    # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação

#beta = [0, 0, 1]
#beta = [0, 0.5, 0.5]
#beta = [0, 1, 0]
beta = [0, 1, 2]

ins = [True, 0, True]     # Linear (True) e não Binário (False)

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal
est_model = 2

predicoes = np.empty(rodadas)
ATE = np.empty(rodadas)

for i in range(rodadas):
	U = np.random.normal(media, var, N)

	yvec = f.simulate(g, model, zvec, beta, ins, U)
	predicoes[i] = f.ate_estimate(g, zvec, yvec, est_model)
	ATE[i] = f.real_ATE(g, model, beta, ins, U)

	print("Rodada {} de {}".format(i+1, rodadas))

media = predicoes.mean()
var = predicoes.var()

fig = plt.figure()
ax = fig.add_subplot(1,1,1,)
n, bins, patches = ax.hist(predicoes, bins=50, histtype='bar')

for patch in patches:
    patch.set_facecolor('y')

vals = "Média: {}\nVariância: {}".format(media, var)
handles, labels = ax.get_legend_handles_labels()
handles.append(mpatches.Patch(color='none', label=vals))
plt.legend(handles=handles)

plt.title('Estimativas do ATE — Email ' + str(beta) + ' Linear Binário')
plt.xlabel("ATE estimado")
plt.ylabel("Número de aparições")
plt.savefig("Imagens/Histograma Email " + str(beta) + " .png")
#plt.show()

# mse = ((predicoes - ATE) ** 2).mean()
# print(mse)