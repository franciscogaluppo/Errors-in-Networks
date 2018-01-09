#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from Funcs.Simulate import simulate
from Funcs.Simulate import real_ATE
from scipy.stats import norm
from sklearn import linear_model
from statsmodels.discrete.discrete_model import Logit
from statsmodels.discrete.discrete_model import Probit

# TODO: 5 e 6 ainda não foram implementadas nesta função
# Estima o valor do ATE
def estimate(g, zvec, yvec, est_model):
    N = len(zvec)

    # SUTVA
    if est_model == 1:
        z1 = 0
        z0 = 0

        sum_resp_z1 = 0
        sum_resp_z0 = 0

        # Soma dos valores
        for i in range(N):
            if zvec[i] == 1:
                z1 += 1
                sum_resp_z1 += yvec[i]
            else:
                z0 += 1
                sum_resp_z0 += yvec[i]

        # Excessões
        if z1 == 0:
            sum_resp_z1 = 0
            z1 = 1

        if z0 == 0:
            sum_resp_z0 = 0
            z0 = 1

        return(sum_resp_z1/z1 - sum_resp_z0/z0)

    # Vetor tau
    tau = np.empty(shape=(N))
    for i in range(N):
        soma = 0.0
        for k in g.neighbors(i):
            soma += np.float64(zvec[k])
        tau[i] = soma/g.degree(i)

    # Vetor das features
    features = np.empty(shape=(N, 3))
    for j in range(N):
        features[j][0] = 1
        features[j][1] = zvec[j]
        features[j][2] = tau[j]

    # Linear
    if est_model == 2:
        lr = linear_model.LinearRegression().fit(features, yvec).coef_
        return(lr[1] + lr[2])

    # Probit
    if est_model == 3:
        vals = Probit(yvec, features).fit(disp=0).params
        return(norm.cdf(sum(vals)) - norm.cdf(vals[0]))

    # Logit
    if est_model == 4:
        vals = Logit(yvec, features).fit(disp=0).params
        return(
            (np.exp(-vals[0]) - np.exp(-sum(vals)))/
            ((1 + np.exp(-vals[0])) * (1 + np.exp(-sum(vals))))
        )


# TODO: Find tau_param
# Execita a estimativa múltiplas vezes
def multiple_estimate(g, zvec, ins, betas, model=3, estimator_types=[1, 2, 3, 4, 5, 6],
                        runs=1000, mean_var=[0, 1], silent=True, tau_param=0): 
    N = g.number_of_nodes()
    
    # Caso seja necessário o vetor frac
    if len([x for x in estimator_types if x in [2, 3, 4]]):
        
        # Vetor frac
        frac = np.empty(shape=(N))
        for i in range(N):
            soma = np.float64(0)
            for k in g.neighbors(i):
                soma += np.float64(zvec[k])
            frac[i] = soma/g.degree(i)

        # Vetor das features
        features = np.empty(shape=(N, 3))
        for j in range(N):
            features[j][0] = 1
            features[j][1] = zvec[j]
            features[j][2] = frac[j]

    # Caso seja o modelo tau
    if len([x for x in estimator_types if x in [5, 6]]):
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

            if zvec[i] == 0 and frac < tau_param:
                z0[i] = 1
            
            elif zvec[i] == 1 and frac > tau_param:
                z1[i] = 1

        # Tamanhos
        tam_z1 = int(sum(z1))
        tam_z0 = int(sum(z0))

        if not tam_z0:
            tam_z0 = 1 
        if not tam_z1:
            tam_z1 = 1

        for i in range(N):
            if z1[i] or z0[i]:
                uniao[i] = 1

        # Caso queira a regressão linear em C1 e C0
        if 6 in estimator_types:
            tam = int(sum(uniao))
            tau = np.empty(shape=(tam))
            feat = np.empty(shape=(tam, 3))
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
                    aux += 1



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
            
                # SUTVA
                if est_model == 1:
                    z1_count = 0
                    z0_count = 0

                    sum_resp_z1 = 0
                    sum_resp_z0 = 0

                    # Soma dos valores
                    for l in range(N):
                        if zvec[l] == 1:
                            z1_count += 1
                            sum_resp_z1 += yvec[l]
                        else:
                            z0_count += 1
                            sum_resp_z0 += yvec[l]

                    # Excessões
                    if z1_count == 0:
                        sum_resp_z1 = 0
                        z1_count = 1

                    if z0_count == 0:
                        sum_resp_z0 = 0
                        z0_count = 1

                    predicoes[i][j][k] = (sum_resp_z1/z1_count - sum_resp_z0/z0_count)

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

                # Diferença das médias
                elif est_model == 5:
                    soma_z1 = 0
                    soma_z0 = 0

                    for l in range(N):
                        if z1[l]:
                            soma_z1 += yvec[l]
                        elif z0[l]:
                            soma_z0 += yvec[l]

                    predicoes[i][j][k] = (soma_z1/tam_z1 - soma_z0/tam_z0)

                # Regressão linear em C1 e C0
                elif est_model == 6:
                    y = np.empty(shape=(tam))
                    aux = 0

                    # Vetor y
                    for l in range(N):
                        if uniao[l]:
                            y[aux] = yvec[l]
                            aux += 1

                    # Regressão
                    lr = linear_model.LinearRegression().fit(feat, y).coef_
                    predicoes[i][j][k] = (lr[1] + lr[2])

                ATE[i][j][k] = real_ATE(g, model, beta, ins, U)

                if not silent:
                    print("est: {}/{}| beta: {}/{}| rodada: {}/{}".format(i+1, len(estimator_types),
                        j+1, len(betas), k+1, runs))
   
    return([predicoes, ATE])

    