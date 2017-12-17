import funcs as f
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = 1000            # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação

betas = [[0, 0, 1], [0, 0.5, 0.5], [0, 1, 0], [0, 1, 1], [0, 1, 2]]
ins = [False, 0.5, True]

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal

X = np.empty(shape=(len(betas), 3, rodadas))
ATE = np.empty(shape=(len(betas), rodadas))

for i in range(len(betas)):
	beta = betas[i]
	for j in range(3):
		for k in range(rodadas):
			U = np.random.normal(media, var, N)
			yvec = f.simulate(g, model, zvec, beta, ins, U)
			X[i][j][k] = f.ate_estimate(g, zvec, yvec, 2 + j)
			ATE[i][k] = f.real_ATE(g, model, beta, ins, U)
			print("Beta: {}/{} | Modelo: {}/{} | Rodada: {}/{}".format(i+1, len(betas), j+1, 3, k+1, rodadas))

mse = np.empty(shape=(len(betas), 3))
for i in range(len(betas)):
	for j in range(3):
		mse[i][j] = ((X[i][j] - ATE) ** 2).mean()

for i in range(len(betas)):
	beta = betas[i]
	arq = open("Comparativos/Modelo_tau(0.5)-email " + str(beta) + ".txt", "w")
	arq.write("# MSE: {}, {}, {}\n# ATE, linear, probit, logit\n".format(mse[i][0], mse[i][1], mse[i][2]))

	for k in range(rodadas):
		arq.write("{}, {}, {}, {}\n".format(ATE[i][k], X[i][0][k], X[i][1][k], X[i][2][k]))
	arq.close()	