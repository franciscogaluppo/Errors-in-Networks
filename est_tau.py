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


# # Diferença de regressões lineares

# tau_z1 = np.empty(shape=(tam_z1))
# tau_z0 = np.empty(shape=(tam_z0))

# feat_z1 = np.empty(shape=(tam_z1, 3))
# feat_z0 = np.empty(shape=(tam_z0, 3))

# y_z1 = np.empty(shape=(tam_z1))
# y_z0 = np.empty(shape=(tam_z0))

# aux_z1 = 0
# aux_z0 = 0

# # Vetor tau
# for i in range(N):
# 	if z1[i]:
# 		soma = 0.0
# 		for k in g.neighbors(i):
# 			soma += np.float64(zvec[k])
# 		tau_z1[aux_z1] = soma/g.degree(i)
# 		aux_z1 += 1

# 	elif z0[i]:
# 		soma = 0.0
# 		for k in g.neighbors(i):
# 			soma += np.float64(zvec[k])
# 		tau_z0[aux_z0] = soma/g.degree(i)
# 		aux_z0 += 1			


# aux_z1 = 0
# aux_z0 = 0

# # Vetor das features
# for i in range(N):
# 	if z1[i]:
# 		feat_z1[aux_z1][0] = 1
# 		feat_z1[aux_z1][1] = zvec[i]
# 		feat_z1[aux_z1][2] = tau_z1[aux_z1]
# 		y_z1[aux_z1] = yvec[i]
# 		aux_z1 += 1

# 	elif z0[i]:
# 		feat_z0[aux_z0][0] = 1
# 		feat_z0[aux_z0][1] = zvec[i]
# 		feat_z0[aux_z0][2] = tau_z0[aux_z0]
# 		y_z0[aux_z0] = yvec[i]
# 		aux_z0 += 1

# # Regressões
# lr_z1 = linear_model.LinearRegression().fit(feat_z1, y_z1).coef_
# lr_z0 = linear_model.LinearRegression().fit(feat_z0, y_z0).coef_

# print(lr_z1[0], lr_z1[1], lr_z1[2], lr_z0[0], lr_z0[1], lr_z0[2])

# ATE_reg = (lr_z1[1] + lr_z1[2]) - (lr_z0[1] + lr_z0[2])
# print("ATE reg: {}".format(ATE_reg))