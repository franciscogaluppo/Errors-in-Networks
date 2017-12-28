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
