import numpy as np
from funcs import simulate
from funcs import real_ATE
from scipy.stats import norm
from sklearn import linear_model
from statsmodels.discrete.discrete_model import Logit
from statsmodels.discrete.discrete_model import Probit

def estimate(g, zvec, ins, betas, model=3, estimator_types=[2, 3, 4], runs=1000, mean_var=[0, 1], silent=True):
    
    N = g.number_of_nodes()
    
    # Caso seja necessário o vetor tau
    if len([x for x in estimator_types if x in [2, 3, 4]]):
        
        # Vetor tau
        tau = []
        for i in range(N):
            soma = np.float64(0)
            for k in g.neighbors(i):
                soma += np.float64(zvec[k])
            tau.append(soma/g.degree(i))

        # Vetor das features
        features = []
        for j in range(N):
            features.append([])
            features[j].append(1)
            features[j].append(zvec[j])
            features[j].append(tau[j])

    # Arrays para os resultados
    predicoes = np.empty(shape=(len(estimator_types), len(betas), runs))
    ATE = np.empty(shape=(len(estimator_types), len(betas), runs))

    # Gera os dados e coloca nos array
    for i in range(len(estimator_types)):
        est_model = estimator_types[i]

        for j in range(len(betas)):
            beta = betas[j]
        
            # Estima
            for k in range(runs):
                U = np.random.normal(mean_var[0], mean_var[1], N)
                yvec = simulate(g, model, zvec, beta, ins, U)
            
                 # Linear
                if est_model == 2:
                    lr = linear_model.LinearRegression().fit(features, yvec).coef_
                    predicoes[i][j][k] = (lr[1] + lr[2])

                # Probit
                elif est_model == 3:
                    vals = Probit(yvec, features).fit(disp=0).params
                    predicoes[i][j][k] = (norm.cdf(sum(vals)) - norm.cdf(vals[0]))

                # Logit
                elif est_model == 4:
                    vals = Logit(yvec, features).fit(disp=0).params
                    predicoes[i][j][k] = ((np.exp(-vals[0]) - np.exp(-sum(vals)))/
                        ((1 + np.exp(-vals[0])) * (1 + np.exp(-sum(vals)))))

                ATE[i][j][k] = real_ATE(g, model, beta, ins, U)

                if not silent:
                    print("est: {}/{}| beta: {}/{}| rodada: {}/{}".format(i+1, len(estimator_types),
                        j+1, len(betas), k+1, runs))
   
    return([predicoes, ATE])









# Estimadores do ATE para o modelo do parâmetro tau

import funcs as f
import numpy as np
from sklearn import linear_model

# Setup
nome = "email-Eu-core"
zvec = f.zfile_to_zvector(nome, 1)
model = 3

g = f.get_graph(nome)
beta = [0, 1, 1]
tau = 0.5
ins = [False, tau, False] #TODO: Binário??
N = g.number_of_nodes()
U = np.random.normal(0, 1, N)

yvec = f.simulate(g, model, zvec, beta, ins, U)
ATE = f.real_ATE(g, model, beta, ins, U)
print("ATE real: {}".format(ATE))

# Bitmaps
z1 = np.zeros(shape=(N))
z0 = np.zeros(shape=(N))
uniao = np.zeros(shape=(N))

# Divide os dois grupos
for i in range(N):
    soma = np.float64(0.0)
    for k in g.neighbors(i):
        soma += zvec[k]
    frac = soma / g.degree(i)

    if zvec[i] == 0 and frac < tau:
        z0[i] = 1
    
    elif zvec[i] == 1 and frac > tau:
        z1[i] = 1

tam_z1 = int(sum(z1))
tam_z0 = int(sum(z0))

if not tam_z0 or not tam_z1:
    print("Erro.")

for i in range(N):
    if z1[i] or z0[i]:
        uniao[i] = 1


# Diferença das médias
soma_z1 = 0
soma_z0 = 0

for i in range(N):
    if z1[i]:
        soma_z1 += yvec[i]
    elif z0[i]:
        soma_z0 += yvec[i]

ATE_diff = soma_z1/tam_z1 - soma_z0/tam_z0
print("ATE est: {}".format(ATE_diff))


# Diferença de regressões lineares
tam = int(sum(uniao))
tau = np.empty(shape=(tam))
feat = np.empty(shape=(tam, 3))
y = np.empty(shape=(tam))
aux = 0

# Vetor tau
for i in range(N):
    if uniao[i]:
        soma = 0.0
        for k in g.neighbors(i):
            soma += np.float64(zvec[k])
        tau[aux] = soma/g.degree(i)
        aux += 1

aux = 0

# Vetor das features
for i in range(N):
    if uniao[i]:
        feat[aux][0] = 1
        feat[aux][1] = zvec[i]
        feat[aux][2] = tau[aux]
        y[aux] = yvec[i]
        aux += 1

# Regressões
lr = linear_model.LinearRegression().fit(feat, y).coef_
ATE_reg = lr[1] + lr[2]
print("ATE reg: {}".format(ATE_reg))








import funcs as f
import numpy as np
from sklearn import linear_model

# Setup
nome = "email-Eu-core"
zvec = f.zfile_to_zvector(nome, 1)
model = 3
rodadas = 1000

g = f.get_graph(nome)
betas = [[0, 0, 1], [0, 0.5, 0.5], [0, 1, 0], [0, 1, 1], [0, 1, 2]]
tau = 0.5
ins = [False, tau, True] #TODO: Binário??
N = g.number_of_nodes()


# Bitmaps
z1 = np.zeros(shape=(N))
z0 = np.zeros(shape=(N))

# Bitmaps
z1 = np.zeros(shape=(N))
z0 = np.zeros(shape=(N))
uniao = np.zeros(shape=(N))

# Divide os dois grupos
for i in range(N):
    soma = np.float64(0.0)
    for k in g.neighbors(i):
        soma += zvec[k]
    frac = soma / g.degree(i)

    if zvec[i] == 0 and frac < tau:
        z0[i] = 1
    
    elif zvec[i] == 1 and frac > tau:
        z1[i] = 1

tam_z1 = int(sum(z1))
tam_z0 = int(sum(z0))

if not tam_z0 or not tam_z1:
    print("Erro.")

for i in range(N):
    if z1[i] or z0[i]:
        uniao[i] = 1


# Diferença das médias
def diff(z1, z0, yvec, N):
    soma_z1 = 0
    soma_z0 = 0

    for i in range(N):
        if z1[i]:
            soma_z1 += yvec[i]
        elif z0[i]:
            soma_z0 += yvec[i]

    return(soma_z1/tam_z1 - soma_z0/tam_z0)


# Diferença das regressões
def reg(uniao, yvec, N):
    tam = int(sum(uniao))
    tau = np.empty(shape=(tam))
    feat = np.empty(shape=(tam, 3))
    y = np.empty(shape=(tam))
    aux = 0

    # Vetor tau
    for i in range(N):
        if uniao[i]:
            soma = 0.0
            for k in g.neighbors(i):
                soma += np.float64(zvec[k])
            tau[aux] = soma/g.degree(i)
            aux += 1

    aux = 0

    # Vetor das features
    for i in range(N):
        if uniao[i]:
            feat[aux][0] = 1
            feat[aux][1] = zvec[i]
            feat[aux][2] = tau[aux]
            y[aux] = yvec[i]
            aux += 1

    # Regressões
    lr = linear_model.LinearRegression().fit(feat, y).coef_
    return(lr[1] + lr[2])


X = np.empty(shape=(len(betas), rodadas))
ATE = np.empty(shape=(len(betas), rodadas))

for i in range(len(betas)):
    beta = betas[i]
    for j in range(rodadas):
        U = np.random.normal(0, 1, N)
        yvec = f.simulate(g, model, zvec, beta, ins, U)
        #X[i][j] = diff(z1, z0, yvec, N)
        X[i][j] = reg(uniao, yvec, N)
        ATE[i][j] = f.real_ATE(g, model, beta, ins, U)
        print("Beta: {}/{} | Rodada: {}/{}".format(i+1, len(betas), j+1, rodadas))

mse = np.empty(shape=(len(betas)))
for i in range(len(betas)):
    mse[i] = ((X[i] - ATE) ** 2).mean()

for i in range(len(betas)):
    beta = betas[i]
    arq = open("Comparativos/Modelo_tau(0.5) Diferença de Regressões Binário-email " + str(beta) + ".txt", "w")
    arq.write("# MSE: {}\n# ATE, Diferença de médias\n".format(mse[i]))

    for k in range(rodadas):
        arq.write("{}, {}\n".format(ATE[i][k], X[i][k]))
    arq.close()







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