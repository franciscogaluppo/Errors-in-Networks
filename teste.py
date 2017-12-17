import funcs as f
import numpy as np

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
def diff(z1, z0, yvec, N):
	soma_z1 = 0
	soma_z0 = 0

	for i in range(N):
		if z1[i]:
			soma_z1 += yvec[i]
		elif z0[i]:
			soma_z0 += yvec[i]

	return(soma_z1/tam_z1 - soma_z0/tam_z0)


X = np.empty(shape=(len(betas), rodadas))
ATE = np.empty(shape=(len(betas), rodadas))

for i in range(len(betas)):
	beta = betas[i]
	for j in range(rodadas):
		U = np.random.normal(0, 1, N)
		yvec = f.simulate(g, model, zvec, beta, ins, U)
		X[i][j] = diff(z1, z0, yvec, N)
		ATE[i][j] = f.real_ATE(g, model, beta, ins, U)
		print("Beta: {}/{} | Rodada: {}/{}".format(i+1, len(betas), j+1, rodadas))

mse = np.empty(shape=(len(betas)))
for i in range(len(betas)):
	mse[i] = ((X[i] - ATE) ** 2).mean()

for i in range(len(betas)):
	beta = betas[i]
	arq = open("Comparativos/Modelo_tau(0.5) Diferença de médias binário-email " + str(beta) + ".txt", "w")
	arq.write("# MSE: {}\n# ATE, Diferença de médias\n".format(mse[i]))

	for k in range(rodadas):
		arq.write("{}, {}\n".format(ATE[i][k], X[i][k]))
	arq.close()	