from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
from Funcs import Manipulate

# Grafo
nome = "email-Eu-core"
g = Sugar.get_graph(Sugar.path(nome))

trat = 1
zvec = IO.zfile_to_zvector(nome, trat)

# Rodadas, número do tratamento e modelo utilizado
rodadas = 100
model = 3

# Betas utilizados
betas = [[0, 0, 1],
        [0, 0.5, 0.5],
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 2]]

# Cores, modelos de estimação, nomes desses modelos, controle
cores = ['r', 'b', 'g', 'y', 'm']
ests = [2, 3, 4]
nomes_modelo = ["Linear Binário", "Probit", "Logit"]
ins = [False, 0.5, True]

# Distribuição
media = 0
var = 1

predicoes, ATE = Estimate.multiple_estimate(
        g, zvec, ins, betas, model, ests, rodadas, [media, var], False, 0.5)

IO.write_results(ATE, predicoes, betas, nomes_modelo, "./")
Manipulate.hist(
        predicoes, ATE, betas, 5, nomes_modelo, "./", nome, cores)
#TODO: print MSE