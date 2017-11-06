#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
import funcs as f
import numpy as np


# FUNÇÕES PARA A ALTURA

# Calcula o módulo da diferença
def distance(a, b):
	diff = a - b
	if diff > 0:
		return diff
	return((-1) * diff)

# Calcula a distância real entre o ATE e o valor estimado pela regressão linear
def real_dist(nome, model, ins, zvec, RUNS=100):
	real = f.real_ATE(model, ins, nome)
        #100FIXME: remove line below
        real2 = ins[1]+ins[2]
        print({'ATE real':real, 'beta+gamma':real2})
	for run in xrange(RUNS):
		esti = f.ate_estimate(zvec, f.simulate(model, zvec, ins, nome), nome, 2)
		if run == 0:
			sum_esti = esti
		else:
			sum_esti += esti
        print([real,sum_esti/RUNS])
	return(distance(real, sum_esti/RUNS))

# Calcula a distância real com a função a() entre o ATE e o valor estimado pela regressão probit
def real_dist_a(nome, model, ins, zvec):
	real = f.real_ATE(model, ins, nome)
	esti = f.ate_estimate(zvec, f.simulate(model, zvec, ins, nome), nome, 3)
	return(distance(real, esti))

# Calcula a distância relativa entre o ATE e o valor estimado pela regressão linear
def relative_dist(nome, model, ins, zvec):
	return(real_dist(nome, model, ins, zvec)/(ins[1] + ins[2]))

# Calcula a fração de respostas 1
def fracz1(nome, model, ins, zvec):
	return(sum(f.simulate(model, zvec, ins, nome)) / len(zvec))



# CÓDIGO PRINCIPAL

# Constantes
nome = "email-Eu-core"	  # Nome do Dataset
trat = 1		  # Número do vetor de tratamento
model = 3		  # Número do modelo da simulação


# Lê o arquivo de tratamento escolhido e retorna o vetor
zvec = f.zfile_to_zvector(nome, trat)


# Vetores observados
betas = []
gammas = []
altura = []


#  -- ENTRADAS

# Modelo 1

# Modelo 2

# Modelo 3
if model == 3:
	ins = [0,      # Alpha
		'beta',    # Beta
		'gamma',   # Gamma
		True,	   # Linear
		0,	   # Tau
		False,	   # Função a
		0,	   # Média µ do U
		0.1]	   # Var σ² do U

# Modelo 4
if model == 4:
	ins = [0,      # Alpha
		'beta',    # Beta
		'gamma',   # Gamma
		10,	   # Tempo discreto
		0,	   # Média µ do U
		0.4]	   # Var σ² do U


#  -- SIMULAÇÕES

# Roda a simulação para diferentes gammas
for gamma in [x / np.float64(10.0) for x in range(1, 11, 1)]:

	# Novo valor de gamma
	ins[2] = gamma

	# E para diferentes betas
	for beta in [x / np.float64(10.0) for x in range(1, 11, 1)]:

		# Novo valor de beta
		ins[1] = beta

		# Adiciona ao vetor
		betas.append(beta)
		gammas.append(gamma)

		# Cálculo da altura usando a função desejada
		altura.append(real_dist(nome, model, ins, zvec))

	print(str(int(gamma*100)) + " %")


#  -- GRÁFICO

# Figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(betas, gammas, altura)

# Legenda
ax.set_xlabel("Beta")
ax.set_ylabel("Gamma")
ax.set_zlabel("Distance")

# Finalização
path = "Imagens/Plots/"
run = len([ x for x in listdir(path)]) + 1
plt.savefig(path + "TESTE #" + str(run) + ".png")
#plt.show()
