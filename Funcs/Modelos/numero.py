#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx

from Comu.comu import comunidade as com

# Função a
def a(valor):
    if valor <= 0: return 0
    return 1


# Função Número
def num(g, beta_vector, ins, zvector, U, comu=None):

    # Entradas
    alpha = beta_vector[0]
    beta = beta_vector[1]
    gama = beta_vector[2]

    # Kappa
    kappa = ins[0]

    if comu != None:
        membros = com(comu)

    N = g.number_of_nodes()

    # Tratamentos
    for i in range(N):
        g.node[i]['z'] = zvector[i]

    # Comunidades    
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