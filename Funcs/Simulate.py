#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from Funcs.Comu.comu import comunidade as com


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
            g.node[i]['y'] = alpha + U[i]
        
        elif g.node[i]['z'] == 1 and frac > tau and not linear:
            g.node[i]['y'] = alpha + beta + U[i]
        
        else:
            g.node[i]['y'] = alpha + beta*g.node[i]['z'] + gama*frac + U[i]

        if binario:
            g.node[i]['y'] = a(g.node[i]['y'])
            
    yvector = np.empty(N)
    for i in range(N):
        yvector[i] = g.node[i]['y']


    return(yvector)



# Função ITR
def itr(g, beta_vector, zvector, U, comu=None):

    # Entradas
    alpha = beta_vector[0]

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

    # Aplica a função ao grafo
    for j in range(N):
        g.node[j]['y'] = a(alpha * g.node[j]['z'] + U[j])

    yvector = []
    for i in range(N):
        yvector.append(g.node[i]['y'])

    return(yvector)


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
            frac = soma / g.degree(i)

            # Aplica a função ao nó j
            g.node[j]["y'"] = a(alpha + (beta * g.node[j]['z']) + (gama * frac) + U[j])

        # Atualiza as respostas dos nós com os novos valores
        for j in range(N):
            g.node[j]['y'] = g.node[j]["y'"]

    yvector = []
    for i in range(N):
        yvector.append(g.node[i]['y'])

    return(yvector)


# Simula um dos modelos
def simulate(g, model, zvec, beta_vector, ins, U=None):
    if model == 1:
        return(itr(g, beta_vector, zvec, U))

    elif model == 2:
        return(num(g, beta_vector, ins, zvec, U))

    elif model == 3:
        return(frac(g, beta_vector, ins, zvec, U))

    elif model == 4:
        return(resp(g, beta_vector, ins, zvec, U))


# Calcula o ATE real
def real_ATE(g, model, beta_vector, ins, U):
    N = g.number_of_nodes()
    return((sum(simulate(g, model, [1]*N, beta_vector, ins, U)) - sum(simulate(g, model, [0]*N, beta_vector, ins, U)))/N)
