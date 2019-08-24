import os
from sys import argv
from Funcs import Sugar
from Funcs import Estimate
import numpy as np

def cria_zvec_comu(nome, p_z0, i):
    comu = open("Comunidades/{}/{}/{}.txt".format(bruno, nome, i), 'r')
    comunidades = [list(map(int, x)) for x in [y.split() for y in comu]]
    comu.close()
    
    trats = np.random.permutation([1*(x >= round(len(comunidades) * p_z0)) for x in range(len(comunidades))])
    n = sum([sum(x) for x in comunidades])
    zvec = np.empty(shape=(n))

    for i in range(len(comunidades)):
        z = trats[i]
        for j in comunidades[i]:
            zvec[j] = z

    return(zvec, trats)

def salva_zvec(zvec, nome, i, j):
    path = "Comunidades/zvecs/{}/{}/".format(bruno, nome)
    if not os.path.exists(path):
        os.makedirs(path)

    run = len(os.listdir(path)) + 1
    arq = open(path+"|{},{}|{}.txt".format(i, j, run), "w")

    for i in range(len(zvec)):
        arq.write(str(zvec[i]))
    arq.close()
    return(run)

# <3
if(len(argv) <3 +1):
    print("[ERRO] Número de parâmtros é menor do que o necessário\nModo de usar: python3 comu.py dataset modelo <tau=0>")
    exit(1)

lixo, nome, modelo, bruno = argv[0:4]
tau = 0 if len(argv) == 4 else float(argv[4])

# Betas utilizados
betas = [
	[0, 0, 1],
	[0, 1, 0.5],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

# Número correspondente a cada estimador
ests_dict = {
	"Linear": 2,
	"Probit": 3,
	"Logit": 4,
	"Tau-Exposure": 5,
	"Tau-Exposure-Binario": 5
}

# Controle para cada modelo_resposta
controles = {
	"Probit": [True, tau, True],
	"Logit": [True, tau, True],
	"Tau-Exposure": [False, tau, False],
	"Tau-Exposure-Binario": [False, tau, True],
	"Linear": [True, tau, False]
}

rodadas = 10
est = [ests_dict[modelo]]
ins = controles[modelo]
g = Sugar.get_graph(Sugar.path(nome))

ATE_total = [np.empty(shape=(1)) for i in range(len(betas))]
est_total = [np.empty(shape=(1)) for i in range(len(betas))]

for i in range(1, 11):
    for j in range(1, 11):
        zvec, trats = cria_zvec_comu(nome, 0.5, i)
        #run = salva_zvec(zvec, nome, i, j)

        # Gera valores
        predicoes, ATE = Estimate.multiple_estimate(
	    g, zvec, ins, betas, 3, est,
	    rodadas, modelo, [0,1], True, tau
        )

        for k in range(len(betas)):
            if len(ATE_total[k]) == 1:
                ATE_total[k] = ATE[0][k]
                est_total[k] = predicoes[0][k]
            else:
                ATE_total[k] = np.concatenate([ATE_total[k], ATE[0][k]])
                est_total[k] = np.concatenate([est_total[k], predicoes[0][k]])
                



path = "Comunidades/Resultados/{}/{}/".format(bruno, nome)

if not os.path.exists(path):
    os.makedirs(path)

arq = open(path+modelo+".txt".format(), "w")
arq.write("{} | {} | {}\n\n".format(bruno, nome, modelo))

for i in range(len(betas)):
    arq.write("{}\nMédia do ATE real: {}\nMédia do ATE estimado: {}\nMSE: {}\n\n".format(
        betas[i], ATE_total[i].mean(), est_total[i].mean(), ((ATE_total[i] - est_total[i])**2).mean() 
        ))

arq.close()
