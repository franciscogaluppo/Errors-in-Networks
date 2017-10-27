#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx

from comu import comunidade as com

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função Número
def num(g, ins, zvector, normal=[0, 1], comu=None):

	# Entradas
	alpha = ins[0]
	beta = ins[1]
	gama = ins[2]
	kappa = ins[3]

	if comu != None:
		membros = com(comu)

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	# Componente Estocástico
	U = np.random.normal(ins[4], ins[5], N)
	if comu != None:
		for k in membros:
			U[k] = np.random.normal(0.5, 0.8)


	for i in range(N):

		# Soma dos tratamentos dos nós vizinhos de i
		soma = 0
		for k in g.neighbors(i): soma += g.node[k]['z']

		# Grupo controle
		if g.node[i]['z'] == 0 and soma < kappa:
			g.node[i]['y'] = a(alpha + U[i])

		# Grupo tratamento
		elif g.node[i]['z'] == 1 and soma > kappa:
			g.node[i]['y'] = a(alpha + beta + U[i])

		# Sobra
		else:
			g.node[i]['y'] = a(alpha + (g.node[i]['z']*gama + (1 - gama)*min(kappa, soma)*beta/(gama + (1 - gama)*kappa) + U[i]))

	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])

	return(yvector)
