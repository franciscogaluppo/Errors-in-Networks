import funcs as f
import numpy as np
from sys import argv

nome = "p2p-Gnutella08"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = int(argv[1])    # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação
beta = [0, 1, 1]          # Vetor Beta
ins = [True, 0, True]     # Linear (True) e não Binário (False)

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal

est_model = 4
predicoes = np.empty(rodadas)
ATE = np.empty(rodadas)

for i in range(rodadas):
	U = np.random.normal(media, var, N)

	yvec = f.simulate(g, model, zvec, beta, ins, U)
	predicoes[i] = f.ate_estimate(g, zvec, yvec, est_model)
	ATE[i] = f.real_ATE(g, model, beta, ins, U)

	print("Rodada {} de {}".format(i+1, rodadas))

mse = ((predicoes - ATE) ** 2).mean()
print(mse)