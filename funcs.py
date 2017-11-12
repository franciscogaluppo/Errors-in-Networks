#!/usr/bin/env python
# -*- coding: utf-8 -*-

from statsmodels.discrete.discrete_model import Probit
from statsmodels.discrete.discrete_model import Logit
from scipy.stats import norm
from random import random as rd
import networkx as nx
from sklearn import linear_model
from os import listdir
# import ipdb
import numpy as np
import sys

from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac
from Modelos.resp_based import resp

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Imprime os resultados
def print_out(model, zvec, yvec):

	out = [count_z1(yvec), count_y1z0(zvec, yvec), count_y1z1(zvec, yvec)]

	# Imprime o nome do modelo
	if model == 1:
		print("\n--ITR")
	elif model == 2:
		print("\n--Números")
	elif model == 3:
		print("\n--Fração")
	elif model == 4:
		print("\n--Response Based")

	# Imprime os resultados
	print("Fração de nós com Yi=1: {}".format(out[0]))

	if out[1] != None:
		print("Fração de nós com Yi=1 dado que Z=0: {}".format(out[1]))
	else:
		print("Não há nós com Z=0")

	if out[2] != None:
		print("Fração de nós com Yi=1 dado que Z=1: {}".format(out[2]))
	else:
		print("Não há nós com Z=1")


# Recebe o vetor beta do usuário
def get_beta_vector(model):
	betas = []
	betas.append(np.float64(input("Alpha: ")))

	# NOT ITR
	if model != 1:
		betas.append(np.float64(input("Beta: ")))
		betas.append(np.float64(input("Gamma: ")))

	return(betas)


# Recebe os controles
def get_input(model):
	inputs = []
	if model == 2:
		inputs.append(np.float64(input("Kappa: ")))

	elif model == 3:
		inputs.append(bool(int(input("Linear: "))))
		inputs.append(0)
		inputs.append(bool(int(input("Função a: "))))

		if inputs[0] == False:
			inputs[1] = (np.float64(input("Tau: ")))

	elif model == 4:
		inputs.append(int(input("Time: ")))

	return(inputs)


# Pede para o usuário os parámetros da Normal
def get_normal_params():
	params = []
	params.append(np.float64(input("µ: ")))
	params.append(np.float64(input("σ²: ")))
	return(params)


# Cria vetor com porcentagem desejada de z=1
def cent(val, N):
	treatment = []

	for i in range(N):
		if rd() < val/100:
			treatment.append(1)
		else:
			treatment.append(0)
	return treatment


# Fração de vértices de z1 em N
def count_z1(vec):
	out = 0
	N = len(vec)

	for i in range(N):
		out += a(vec[i])
	return(out/N)


# Fração de vértives de z1 que foram y1
def count_y1z1(vecz, vecy):
	out = 0
	div = 0
	N = len(vecz)

	for i in range(N):
		if(vecz[i] == 1):
			out += a(vecy[i])
			div += 1

	if div != 0:
		return(out/div)
	return(None)


# Fração de vértives de z0 que foram y1
def count_y1z0(vecz, vecy):
	out = 0
	div = 0
	N = len(vecz)

	for i in range(N):
		if(vecz[i] == 0):
			out += a(vecy[i])
			div += 1

	if div != 0:
		return(out/div)
	return(None)


# Estima o valor do ATE
def ate_estimate(g, zvec, yvec, est_model):
	N = len(zvec)

	# SUTVA
	if est_model == 1:
		z1 = 0
		z0 = 0

		sum_resp_z1 = 0
		sum_resp_z0 = 0

		# Soma dos valores
		for i in range(N):
			if zvec[i] == 1:
				z1 += 1
				sum_resp_z1 += yvec[i]
			else:
				z0 += 1
				sum_resp_z0 += yvec[i]

		# Excessões
		if z1 == 0:
			sum_resp_z1 = 0
			z1 = 1

		if z0 == 0:
			sum_resp_z0 = 0
			z0 = 1

		return(sum_resp_z1/z1 - sum_resp_z0/z0)

	# Vetor tau
	tau = []
	for i in range(N):
		soma = 0.0
		for k in g.neighbors(i):
			soma += np.float64(zvec[k])
			
		if g.degree(i) == 0:
			tau.append(1.0)
		else:
			tau.append(soma/g.degree(i))

	# Vetor das features
	features = []
	for j in range(N):
		features.append([])
		features[j].append(1.0)
		features[j].append(zvec[j])
		features[j].append(tau[j])

	# Linear
	if est_model == 2:
		lr = linear_model.LinearRegression().fit(features, yvec).coef_
		return(lr[1] + lr[2])

	# Probit
	if est_model == 3:
		vals = Probit(yvec, features).fit(disp=0).params
		return(norm.cdf(sum(vals)) - norm.cdf(vals[0]))

	# Logit
	if est_model == 4:
		vals = Logit(yvec, features).fit(disp=0).params
		return(
			(np.exp(-vals[0]) - np.exp(-sum(vals)))/
			((1 + np.exp(-vals[0])) * (1 + np.exp(-sum(vals))))
		)



# Cria path completo do set
def path(name):
	return("Datasets/" + name + "/set.txt")


# Cria str com zero à esquerda se n < 10
def int_to_str(run):
	if run < 10:
		return("0" + str(run))
	return(str(run))


# Cria o arquivo do zvector
def zvector_to_zfile(vec, name):
	N = len(vec)
	path = "Datasets/" + name + "/Tratamentos/"
	run = len(listdir(path)) + 1

	# Zero à esquerda
	run = int_to_str(run)

	path += "Z-#" + run + ".txt"
	arq = open(path, "w")

	# Escreve no arquivo
	for i in range(N):
		arq.write("{}\n".format(vec[i]))
	arq.close()

	return(int(run))


# Cria zvector lendo de um arquivo
def zfile_to_zvector(name, run):
	treatment = []

	# Zero à esquerda
	run = int_to_str(run)

	path = "Datasets/" + name + "/Tratamentos/Z-#" + run + ".txt"
	tf = open(path, "r")

	# Lê o arquivo
	for i in tf:
		treatment.append(int(i[0]))

	tf.close()
	return(treatment)


# Cria o arquivo do ins
def beta_vector_to_file(beta_vector, name, model):
	N = len(beta_vector)
	path = "Datasets/" + name + "/Betas/"
	run = len([ x for x in listdir(path) if ("m" +  str(model)) in x ]) + 1

	# Zero à esquerda
	run = int_to_str(run)

	path += "Beta-m" + str(model) + "|#" + run + ".txt"
	arq = open(path, "w")

	# Escreve no arquivo
	for i in range(N):
		arq.write("{}\n".format(beta_vector[i]))
	arq.close()

	return(int(run))


# Cria ins lendo de um arquivo
def file_to_beta_vector(name, model, run):
	beta_vector = []

	# Zero à esquerda
	run = int_to_str(run)

	path = "Datasets/" + name + "/Betas/Beta-m" + str(model) + "|#" + run + ".txt"
	tf = open(path, "r")

	# Lê o arquivo
	for i in tf:
		if i[0] is "T":
			beta_vector.append(bool(1))
		elif i[0] is "F":
			beta_vector.append(bool(0))
		elif model is 4 and "." not in i:
			beta_vector.append(int(i))
		else:
			beta_vector.append(np.float64(i))
	tf.close()

	return(beta_vector)


# Cria o arquivo do ins
def ins_to_file(ins, name, model):
	if model == 1:
		return(-1)

	N = len(ins)
	path = "Datasets/" + name + "/Ins/"
	run = len([ x for x in listdir(path) if ("m" +  str(model)) in x ]) + 1

	# Zero à esquerda
	run = int_to_str(run)

	path += "ins-m" + str(model) + "|#" + run + ".txt"
	arq = open(path, "w")

	# Escreve no arquivo
	for i in range(N):
		arq.write("{}\n".format(ins[i]))
	arq.close()

	return(int(run))


# Cria ins lendo de um arquivo
def file_to_ins(name, model, run):
	ins = []

	# Zero à esquerda
	run = int_to_str(run)

	path = "Datasets/" + name + "/Ins/ins-m" + str(model) + "|#" + run + ".txt"
	tf = open(path, "r")

	# Lê o arquivo
	for i in tf:
		if i[0] is "T":
			ins.append(bool(1))
		elif i[0] is "F":
			ins.append(bool(0))
		elif model is 4 and "." not in i:
			ins.append(int(i))
		else:
			ins.append(np.float64(i))
	tf.close()

	return(ins)


# Cria o arquivo resposta
def yvector_to_yfile(vec, modelo, name, ins_run, zvec_run, beta_run):
	N = len(vec)
	path = "Datasets/" + name + "/Respostas/"
	zvec_run = int_to_str(zvec_run)
	ins_run = int_to_str(ins_run)
	beta_run = int_to_str(beta_run)

	run = len([ x for x in listdir(path) if ("m" +  str(modelo)) in x
	and ("Z#" + zvec_run) in x and ("ins#" + ins_run) in x]) + 1

	run = int_to_str(run)

	path += "Y-m" + str(modelo) + "|Z#" + zvec_run + "|ins#" + ins_run + "|beta#" + beta_run + "|#" + run + ".txt"
	arq = open(path, "w")

	# Escreve no arquivo
	for i in range(N):
		arq.write("{}\n".format(vec[i]))
	arq.close()

	return(int(run))


# Criva o yvector a partir de um arquivo de resposta
def yfile_to_yvector(name, yvec_run, modelo, ins_run, zvec_run):
	vec = []

	# Zero à esquerda
	yvec_run = int_to_str(yvec_run)
	zvec_run = int_to_str(zvec_run)
	ins_run = int_to_str(ins_run)

	path = "Datasets/" + name + "/Respostas/Y-m" + str(modelo) + "|Z#" + zvec_run + "|ins#" + ins_run + "|beta#" + beta_run + "|#" + yvec_run + ".txt"
	tf = open(path, "r")

	# Lê o arquivo
	for i in tf:
		vec.append(np.float64(i))
	tf.close()
	return(vec)


# Simula um dos modelos
def simulate(g, model, zvec, beta_vector, ins, U=None):
	if model == 1:
		return(np.array(itr(g, beta_vector, zvec, U)))

	elif model == 2:
		return(np.array(num(g, beta_vector, ins, zvec, U)))

	elif model == 3:
		return(np.array(frac(g, beta_vector, ins, zvec, U)))

	elif model == 4:
		return(np.array(resp(g, beta_vector, ins, zvec, U)))


# Calcula o ATE real
def real_ATE(g, model, beta_vector, ins, U):
	N = g.number_of_nodes()
	return((sum(simulate(g, model, [1]*N, beta_vector, ins, U)) - sum(simulate(g, model, [0]*N, beta_vector, ins, U)))/N)


# Inicializa o grafo
def get_graph(name):
	g = nx.read_edgelist(path(name), nodetype=int)

	selfloops = [ (i,i) for i in g.nodes_with_selfloops()]
	g.remove_edges_from(selfloops)

	return(g)


# Calcula a variância
def var_linear(g, zvec, yvec, betas):
	N = len(zvec)

	# Vetor tau
	tau = []
	for i in range(N):
		soma = 0.0
		for k in g.neighbors(i):
			soma += np.float64(zvec[k])
			
		if g.degree(i) == 0:
			tau.append(1.0)
		else:
			tau.append(soma/g.degree(i))

	# Soma dos quadrados das diferenças
	soma = 0
	for i in range(N):
		soma += (yvec[i] - (betas[0] + zvec[i]*betas[1] + tau[i]*betas[2])) ** 2

	return(soma/N)