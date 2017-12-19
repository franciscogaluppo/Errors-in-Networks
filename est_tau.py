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