#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from Comu.comu import comunidade as com
#import csv

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função Fração
def frac(g, beta_vector, ins, zvector, U, comu=None):

	# Ceoeficientes
	alpha = beta_vector[0]
	beta = beta_vector[1]
	gama = beta_vector[2]

	# Controles
	linear = ins[0]
	tau = ins[1]
	binario = ins[2]

	if comu != None:
		membros = com(comu)

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	# Comunidades - Arbitrátrio
	if comu != None:
		for k in range(N):
			if k in membros:
				U[k] = np.random.normal(0.5, 0.8)

	for i in range(N):
		soma = np.float64(0.0)
		for k in g.neighbors(i): soma += g.node[k]['z']
		
		frac = soma / g.degree(i)

		if g.node[i]['z'] == 0 and frac < tau and not linear:
			g.node[i]['y'] = a(alpha + U[i])
		
		elif g.node[i]['z'] == 1 and frac > tau and not linear:
			g.node[i]['y'] = a(alpha + beta + U[i])
		
		elif binario:
			g.node[i]['y'] = a(alpha + beta*g.node[i]['z'] + gama*frac + U[i])
		
		else:
			g.node[i]['y'] = alpha + beta*g.node[i]['z'] + gama*frac + U[i]
			
	yvector = np.empty(N)
	for i in range(N):
		yvector[i] = g.node[i]['y']


	return(yvector)
