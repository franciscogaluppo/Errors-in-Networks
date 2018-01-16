from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
from Funcs import Manipulate

# Grafo
nome = "p2p-Gnutella08"
g = Sugar.get_graph(Sugar.path(nome))

trat = 2
zvec = IO.zfile_to_zvector(nome, trat)

# Rodadas, número do tratamento e modelo utilizado
rodadas = 1000
model = 3

# Betas utilizados
betas = [[0, 0, 1],
        [0, 0.5, 0.5],
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 2]]

# Modelos de estimação, nomes desses modelos, controle
ests = [1, 2, 3, 4, 5, 6]
modelos =  ["SUTVA",
            "Linear",
            "Probit",
            "Logistic",
            "SUTVA C1 C0",
            "Linear C1 C0"]
ins = [False, 0.5, True]

# Distribuição
media = 0
var = 1

predicoes, ATE = Estimate.multiple_estimate(
        g, zvec, ins, betas, model, ests, rodadas, [media, var], False, 0.5)

for j in range(len(betas)):
    print("MSE {}\n".format(betas[j]))
    for i in range(len(modelos)):
        print("{}: {}".format(modelos[i], ((predicoes[i][j] - ATE[i][j])**2).mean()))
    print()


IO.write_results(ATE, predicoes, betas, modelos, "Resultados/Compara_MSE")