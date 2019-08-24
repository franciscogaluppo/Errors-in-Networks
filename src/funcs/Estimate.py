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
def multiple_estimate(g, zvec, ins, betas, model=3, estimator_types=[1, 2, 3, 4, 5],
                        runs=1000, estoc_distr="Probit", estoc_params=[0, 1], silent=True, tau_param=0.5): 
    N = g.number_of_nodes()
    if model == 3 and estoc_distr in ["Tau-Exposure", "Tau-Exposure-Binario"]:
        tau_param = ins[1]

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
    if 5 in estimator_types:
        # Bitmaps
        c1 = np.zeros(shape=(N))
        c0 = np.zeros(shape=(N))

        # Divide os dois grupos
        for i in range(N):
            soma = np.float64(0.0)
            for k in g.neighbors(i):
                soma += np.float64(zvec[k])
            frac = soma / g.degree(i)

            if zvec[i] == 0 and frac <= (1 - tau_param):
                c0[i] = 1
            
            elif zvec[i] == 1 and frac >= tau_param:
                c1[i] = 1

        # Tamanhos
        tam_c1 = int(sum(c1))
        tam_c0 = int(sum(c0))

        if tam_c0 == 0:
            tam_c0 = 1 
        if tam_c1 == 0:
            tam_c1 = 1


    # Arrays para os resultados
    predicoes = np.empty(shape=(len(estimator_types), len(betas), runs))
    ATE = np.empty(shape=(len(estimator_types), len(betas), runs))

    # Gera os dados e coloca nos array
    for j in range(len(betas)):
        beta = betas[j]
    
        cons1 = 1.0/(1.0 + np.exp(- sum(beta)))
        cons2 = 1.0/(1.0 + np.exp(- beta[0]))

        # Estima
        for k in range(runs):
            if estoc_distr == "Logit":
                U = np.random.uniform(0.0, 1.0, N)
                yvec = np.array([1*(U[x] < (1.0/(1.0 + np.exp(- np.dot(features[x], beta))))) for x in range(N)])
            
                Zigual1 = np.array([1*(U[x] < cons1) for x in range(N)])
                Zigual0 = np.array([1*(U[x] < cons2) for x in range(N)])
                real = (sum(Zigual1) - sum(Zigual0))/N

            else:
                U = np.random.normal(estoc_params[0], estoc_params[1], N)
                yvec = simulate(g, model, zvec, beta, ins, U)
                real = real_ATE(g, model, beta, ins, U)

            for i in range(len(estimator_types)):
                est_model = estimator_types[i]

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
                elif est_model == 2:
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

                # Tau exposure
                elif est_model == 5:
                    soma_c1 = 0
                    soma_c0 = 0

                    for l in range(N):
                        if c1[l] == 1:
                            soma_c1 += yvec[l]
                        elif c0[l] == 1:
                            soma_c0 += yvec[l]

                    predicoes[i][j][k] = (soma_c1/tam_c1 - soma_c0/tam_c0)

                ATE[i][j][k] = real
        
                if not silent:
                    print("est: {}/{}| beta: {}/{}| rodada: {}/{}".format(i+1, len(estimator_types),
                        j+1, len(betas), k+1, runs))
   
    return([predicoes, ATE])
