import funcs as f
import numpy as np
from estimate import estimate
import matplotlib.pyplot as plt
import time

nome = "email-Eu-core"      # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = 1000            # Número de rodadas
trat = 1                    # Número do vetor de tratamento
ins = [True, 0, True]
zvec = f.zfile_to_zvector(nome, trat)
betas = [[0, 0, 1], [0, 0.5, 0.5], [0, 1, 0], [0, 1, 1], [0, 1, 2]]

a = time.clock()
teste = estimate(g, zvec, ins, betas)
b = time.clock()

print(b - a)

X = teste[0]
ATE = teste[1]

# mse = np.empty(shape=(len(betas), 3))
# for i in range(len(betas)):
#     for j in range(3):
#         mse[i][j] = ((X[i][j] - ATE) ** 2).mean()


# for i in range(len(betas)):
#     beta = betas[i]
#     arq = open("Comparativos/Modelo_tau(0.5)-email " + str(beta) + ".txt", "w")
#     arq.write("# MSE: {}, {}, {}\n# ATE, linear, probit, logit\n".format(mse[i][0], mse[i][1], mse[i][2]))

#     for k in range(rodadas):
#         arq.write("{}, {}, {}, {}\n".format(ATE[i][k], X[i][0][k], X[i][1][k], X[i][2][k]))
#     arq.close()    