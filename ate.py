import funcs as f
import networkx as nx
from sklearn import linear_model

def ate_estimate(zvec, yvec, g, est_model):
	N = len(zvec)

	# SUTVA
	if est_model == 1:
		sum_z1 = 0
		sum_z0 = 0

		sum_resp_z1 = 0
		sum_resp_z0 = 0

		for i in range(N):
			if zvec[i] == 1:
				sum_z1 += 1
				sum_resp_z1 += yvec[i]
			else:
				sum_z0 += 1
				sum_resp_z0 += yvec[i]

		if not sum_z1 or not sum_z0:
			return(-1)
		return(sum_resp_z1/sum_z1 - sum_resp_z0/sum_z0)

	# Linear
	if est_model == 2:

		# Vetor tau
		tau = []
		for i in range(N):
			soma = 0
			for k in g.neighbors(i):
				soma += zvec[k]
			tau.append(soma/g.degree(i))

		# Vetor das features
		features = []
		for j in range(N):
			features.append([])
			features[j].append(zvec[j])
			features[j].append(tau[j])

		# Regressão
		lr = linear_model.LinearRegression()
		lr.fit(features, yvec)
		
		c = lr.coef_
		i = lr.intercept_ 

		# Constantes
		alpha = i
		beta = c[0]
		gama = c[1]

		# Cálculo da estimativa
		sum_resp_z1 = 0
		sum_resp_z0 = 0

		for i in range(N):
			soma = 0
			for k in g.neighbors(i): soma += zvec[k]

			if zvec[i] == 1:
				sum_resp_z1 += alpha + beta + (gama * tau[i])
			else:
				sum_resp_z0 += alpha + (gama * tau[i])

		return((sum_resp_z1 - sum_resp_z0)/N)