import funcs as f
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = 1000            # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação

#beta = [0, 0, 1]
#beta = [0, 0.5, 0.5]
#beta = [0, 1, 0]
beta = [0, 1, 1]

ins = [True, 0, True]     # Linear (True) e não Binário (False)

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal


X = np.empty((3, rodadas))
ATE = np.empty(rodadas)

for i in range(rodadas):
	for j in range(3):
		U = np.random.normal(media, var, N)

		yvec = f.simulate(g, model, zvec, beta, ins, U)
		X[j][i] = f.ate_estimate(g, zvec, yvec, 2 + j)
	
	ATE[i] = f.real_ATE(g, model, beta, ins, U)
	print("Rodada {} de {}".format(i+1, rodadas))


mse = np.empty(3)
for i in range(3): 
	mse[i] = ((X[i] - ATE) ** 2).mean()

arq = open("Comparativos/Binario-email " + str(beta) + ".txt", "w")
arq.write("# MSE: {}, {}, {}\n# ATE, linear, probit, logit\n".format(mse[0], mse[1], mse[2]))

for i in range(rodadas):
	arq.write("{}, {}, {}, {}\n".format(ATE[i], X[0][i], X[1][i], X[2][i]))
arq.close()	

print("# MSE: {}, {}, {}".format(mse[0], mse[1], mse[2]))
