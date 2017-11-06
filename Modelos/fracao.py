#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from comu import comunidade as com
#import csv

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


# Função Fração
def frac(g, ins, zvector, U, comu=None):

	# Entradas
	alpha = ins[0]
	beta = ins[1]
	gama = ins[2]
	linear = ins[3]
	tau = ins[4]
	binario = ins[5]

	if comu != None:
		membros = com(comu)

	N = g.number_of_nodes()

	# Tratamentos
	for i in range(N):
		g.node[i]['z'] = zvector[i]

	# Componente Estocástico
	if U == None:
		U = np.random.normal(ins[6], ins[7], N)

	if comu != None:
		for k in range(N):
			if k in membros:
				U[k] = np.random.normal(0.5, 0.8)


	#filename = 'a{0}_b{1}_g{2}.txt'.format(alpha, beta, gama)
	#with open(filename,'w') as csvfile:
	#	datafile = csv.writer(csvfile)
	for i in range(N):
		soma = np.float64(0.0)
		for k in g.neighbors(i): soma += g.node[k]['z']
		#TODO: decide for isolated nodes if fraction should be 0 or 1
		frac = soma / g.degree(i) if g.degree(i) else 1
		if g.node[i]['z'] == 0 and frac < tau and not linear:
			g.node[i]['y'] = a(alpha + U[i])
		elif g.node[i]['z'] == 1 and frac > tau and not linear:
			g.node[i]['y'] = a(alpha + beta + U[i])
		elif binario:
			g.node[i]['y'] = a(alpha + beta*g.node[i]['z'] + gama*frac + U[i])
		else:
			g.node[i]['y'] = alpha + beta*g.node[i]['z'] + gama*frac + U[i]
			#datafile.writerow([g.node[i]['z'],frac,g.node[i]['y']])

	yvector = []
	for i in range(N):
		yvector.append(g.node[i]['y'])


	return(yvector)
