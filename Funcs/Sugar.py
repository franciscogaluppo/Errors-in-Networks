#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from random import random as rd

# Função a
def a(valor):
    if valor <= 0: return 0
    return 1

# Cria vetor com porcentagem desejada de z=1
def cent(val, N):
    treatment = np.empty(shape=(N))

    for i in range(N):
        if rd() < val/100:
            treatment[i] = 1
        else:
            treatment[i] = 0
    return treatment


# Cria path completo do set
def path(name):
    return("Datasets/" + name + "/set.txt")


# Cria str com zero à esquerda se n < 10
def int_to_str(run):
    if run < 10:
        return("0" + str(run))
    return(str(run))


# Renomeia nós
def relabel(g):
    N = g.number_of_nodes()
    antigo = g.nodes()

    mapping = {node: idx for idx, node in enumerate(g.nodes())}
    return(nx.relabel_nodes(g, mapping))


# Inicializa o grafo
def get_graph(path):
    g = relabel(nx.read_edgelist(path, nodetype=int))
    N = g.number_of_nodes()

    # Remove self loops
    selfloops = [ (i,i) for i in g.nodes_with_selfloops()]
    g.remove_edges_from(selfloops)

    # Remove vértices isolados
    for i in range(N):
        if not g.degree(i):
            g.remove_node(i)

    return(relabel(g))


# Calcula a variância
def var_linear(g, zvec, yvec, betas):
    N = len(zvec)

    if len(betas) != 3:
        print("TODO")
        return

    # Vetor tau
    tau = []
    for i in range(N):
        soma = 0.0
        for k in g.neighbors(i):
            soma += np.float64(zvec[k])
        tau.append(soma/g.degree(i))

    # Soma dos quadrados das diferenças
    soma = 0
    for i in range(N):
        soma += (yvec[i] - (betas[0] + zvec[i]*betas[1] + tau[i]*betas[2])) ** 2

    return(soma/(N-1))
