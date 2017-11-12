#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
import funcs as f
import numpy as np
from sys import argv



#  --  FUNÇÕES PARA A ALTURA

# Calcula o módulo da diferença
def distance(a, b):
	diff = a - b
	if diff > 0:
		return diff
	return((-1) * diff)

# Calcula a distância real entre o ATE e o valor estimado pela regressão linear
def real_dist(g, nome, model, ins, betas, zvec, U):
	real = f.real_ATE(g, model, betas, ins, U)
	esti = f.ate_estimate(g, zvec, f.simulate(g, model, zvec, betas, ins, U), 2)
	return(distance(real, esti))

# Calcula a distância real com a função a() entre o ATE e o valor estimado pela regressão probit
def real_dist_probit(g, nome, model, ins, betas, zvec, U):
	real = f.real_ATE(g, model, betas, ins, U)
	esti = f.ate_estimate(g, zvec, f.simulate(g, model, zvec, betas, ins, U), 3)
	return(distance(real, esti))

# Calcula a distância real com a função a() entre o ATE e o valor estimado pela regressão logit
def real_dist_logit(g, nome, model, ins, betas, zvec, U):
	real = f.real_ATE(g, model, betas, ins, U)
	esti = f.ate_estimate(g, zvec, f.simulate(g, model, zvec, betas, ins, U), 4)
	return(distance(real, esti))

# Calcula a distância relativa entre o ATE e o valor estimado pela regressão linear
def relative_dist(g, nome, model, ins, betas, zvec, U):
	return(real_dist(g, nome, model, ins, zvec, U)/(ins[1] + ins[2]))

# Calcula a fração de respostas 1
def fracz1(g, nome, model, ins, betas, zvec, U):
	return(sum(f.simulate(g, model, zvec, betas, ins, U)) / len(zvec))



#  --  CONSTANTES

nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação
N = g.number_of_nodes()

media = 0                 # Média da distribuição Normal
sig_sqd = 0.3             # Variância da distribuição Normal

if len(argv) > 1:
	media, sig_sqd = [np.float64(x) for x in argv[1:3]]

print(media, sig_sqd)
U = np.random.normal(media, sig_sqd, N)


# Lê o arquivo de tratamento escolhido e retorna o vetor
zvec = f.zfile_to_zvector(nome, trat)

# Vetores observados
betas = []
gammas = []
altura = []



#  -- ENTRADAS

# Modelo 3 - Fração
if model == 3:
	ins = [True, 0, True]
	beta_vector = [0, 'beta', 'gamma']

# Modelo 4 - Iterativo
elif model == 4:
	ins = [10]
	beta_vector = [0, 'beta', 'gamma']



#  -- SIMULAÇÕES

# Gammas
for gamma in [x / np.float64(10.0) for x in range(1, 11, 1)]:
	beta_vector[2] = gamma

	# Betas
	for beta in [x / np.float64(10.0) for x in range(1, 11, 1)]:

		beta_vector[1] = beta
		betas.append(beta)
		gammas.append(gamma)

		# Cálculo da altura usando a função desejada
		altura.append(real_dist_logit(g, nome, model, ins, beta_vector, zvec, U))

	#print(str(int(gamma*100)) + "%")



#  -- GRÁFICO

# Figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(betas, gammas, altura)

# Legenda
ax.set_xlabel("Beta")
ax.set_ylabel("Gamma")
#ax.set_zlabel("Distance")

# Finalização
path = "Imagens/Plots/"
run = len([ x for x in listdir(path) if nome in x]) + 1
plt.savefig(path + nome + "|N(" + str(media) + "," + str(sig_sqd) + ")|run#" + str(run) + ".png")
#plt.show()