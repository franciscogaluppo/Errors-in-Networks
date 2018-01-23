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
def hist(predicoes, ATE, betas, bins, nomes_modelos, path="Imagens/Histogramas/", nome_grafo="email-Eu-core", cores=None):
    plt.rcParams.update({'figure.max_open_warning': 0})
    ests, bet_len, rodadas = predicoes.shape
    cor = 'r'

    for i in range(ests):
        modelo = nomes_modelos[i]

        for j in range(bet_len):
            beta = betas[j]
            
            if cores != None:
                cor = cores[j]
            
            # Cálculo de valores
            ATE_est = predicoes[i][j].mean()
            ATE_real = ATE[i][j].mean()
            erro = np.absolute(predicoes[i][j] - ATE[i][j]).mean()
            var = predicoes[i][j].var()

            # Histograma
            fig, ax = plt.subplots() 
            plt.xlabel("ATE estimado")
            plt.ylabel("Frequência")
            n, bins, patches = ax.hist(predicoes[i][j], bins=bins, histtype='bar')
            plt.axvline(ATE_real, color='black', linestyle='dashed', linewidth=2)

            # cores
            for patch in patches:
                patch.set_facecolor(cor)

            # Legenda
            vals = "Média do ATE estimado: {:.5}\nMédia do ATE real: {:.5}\nErro Médio: {:.5}\nVariância: {:.5}\n".format(ATE_est, ATE_real, erro, var)
            handles, labels = ax.get_legend_handles_labels()
            handles.append(mpatches.Patch(color='none', label=vals))
            plt.legend(handles=handles, fontsize=6)

            # Gera o gráfico
            plt.title('Estimativas do ATE — ' + nome_grafo + " " + str(beta) + " " + modelo)
            plt.savefig(path + modelo + " " + nome_grafo + " " + str(beta) + " .png")


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