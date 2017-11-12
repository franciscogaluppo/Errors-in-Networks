#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx

from comu import comunidade as com

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função Response Based
def resp(g, beta_vector, ins, zvector, U, comu=None):

	# Entradas
	alpha = beta_vector[0]
	beta = beta_vector[1]
	gama = beta_vector[2]

	# Tempo
	T = ins[0]

	if comu != None:
		membros = com(comu)

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]
		g.node[i]['y'] = 0

	# Comunidades
	if comu != None:
		for k in membros:
			U[k] = np.random.normal(0.5, 0.8)

	for i in range(T):

		# Aplica a função ao grafo
		for j in range(N):

			# Soma dos tratamentos dos nós vizinhos de j
			soma = np.float64(0.0)
			for k in g.neighbors(j): soma += g.node[k]['y']
			frac = soma / g.degree(i) if g.degree(i) else 1

			# Aplica a função ao nó j
			g.node[j]["y'"] = a(alpha + (beta * g.node[j]['z']) + (gama * frac) + U[j])

		# Atualiza as respostas dos nós com os novos valores
		for j in range(N):
			g.node[j]['y'] = g.node[j]["y'"]

	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])

	return(yvector)
