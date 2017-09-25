import funcs as f
import networkx as nx

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

		return(sum_resp_z1/sum_z1 - sum_resp_z0/sum_z0)

	# Linear
	if est_model == 2:

		# Temporário
		alpha = -0.5
		beta = 0.5
		gama = 0.5

		sum_resp_z1 = 0
		sum_resp_z0 = 0

		for i in range(N):
			soma = 0
			for k in g.neighbors(i): soma += zvec[k]

			if zvec[i] == 1:
				sum_resp_z1 += f.a(alpha + beta + (gama * soma / g.degree(i)))
			else:
				sum_resp_z0 += f.a(alpha + (gama * soma / g.degree(i)))

		return((sum_resp_z1 - sum_resp_z0)/N)