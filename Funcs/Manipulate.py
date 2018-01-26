#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir

import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches


# Cria os histogramas
def hist(predicoes, ATE, betas, bins, nomes_modelos, nome_grafo, estimado_por, path="Imagens/Histogramas/", cores=None):
    plt.rcParams.update({'figure.max_open_warning': 0})
    ests, bet_len, rodadas = predicoes.shape
    cor = 'r'

    for i in range(ests):
        modelo = nomes_modelos[i]

        for j in range(bet_len):
            beta = betas[j]
            
            # print(modelo, beta, predicoes, ATE)
            if cores != None:
                cor = cores[j]
            
            # Cálculo de valores
            ATE_est = predicoes[i][j].mean()
            ATE_real = ATE[i][j].mean()
            erro = ((predicoes[i][j] - ATE[i][j])**2).mean()
            var = predicoes[i][j].var()

            # Histograma
            fig, ax = plt.subplots() 
            plt.xlabel("ATE estimado")
            plt.ylabel("Frequência Relativa")

            n, b, patches = ax.hist(predicoes[i][j], bins=bins, histtype='bar',
                weights=np.zeros_like(predicoes[i][j]) + 1. / predicoes[i][j].size)
            plt.axvline(ATE_real, color='black', linestyle='dashed', linewidth=2)

            # cores
            for patch in patches:
                patch.set_facecolor(cor)

            # Legenda
            vals = "Média do ATE estimado: {:.3}\nMédia do ATE real: {:.3}\nMSE Empírico: {:.3}\nVariância: {:.3}\n".format(ATE_est, ATE_real, erro, var)
            handles, labels = ax.get_legend_handles_labels()
            handles.append(mpatches.Patch(color='none', label=vals))
            plt.legend(handles=handles, fontsize=8, frameon=False)

            # Gera o gráfico
            plt.title("{} - {}({}, {}, {}) - {}". format(nome_grafo, estimado_por, beta[0],
            beta[1], beta[2], modelo))
            plt.savefig("{}{} - {}({}, {}, {}) - {}". format(path, nome_grafo, estimado_por, beta[0],
            beta[1], beta[2], modelo) + ".png")


# Calcula o MSE -- muios parâmetros...
def mse(nome, rodadas, zvec, beta, ins, model, est_model, media, var):
    g = get_graph(nome)
    N = g.number_of_nodes()

    predicoes = np.empty(rodadas)
    ATE = np.empty(rodadas)

    for i in range(rodadas):
        U = np.random.normal(media, var, N)

        yvec = f.simulate(g, model, zvec, beta, ins, U)
        predicoes[i] = f.ate_estimate(g, zvec, yvec, est_model)
        ATE[i] = f.real_ATE(g, model, beta, ins, U)

    return(((predicoes - ATE) ** 2).mean())