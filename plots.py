import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
import funcs as f


# FUNÇÕES PARA A ALTURA

# Calcula o módulo da diferença
def distance(a, b):
	diff = a - b
	if diff > 0:
		return diff
	return((-1) * diff)

# Calcula a distância real
def real_dist(nome, model, ins, zvec):
	real = f.real_ATE(model, ins, nome)
	esti = f.ate_estimate(zvec, f.simulate(model, zvec, ins, nome), nome, 2)
	return(distance(real, esti))

# Calcula a distância relativa
def relative_dist(nome, model, ins, zvec):
	real = f.real_ATE(model, ins, nome)
	esti = f.ate_estimate(zvec, f.simulate(model, zvec, ins, nome), nome, 2)
	return(distance(real, esti)/(ins[1] + ins[2]))

# Calcula a fração de respostas 1
def fracz1(nome, model, ins, zvec):
	return(sum(f.simulate(model, zvec, ins, nome))/len(zvec))


# Constantes
nome = "email-Eu-core"
trat = 6
model = 3

# m3
ins = [0, 'beta', 'gamma', True, 0, False, 0, 0.4]

# m4
# ins = [0, 'beta', 'gamma', 10, 0, 0.4]

zvec = f.zfile_to_zvector(nome, trat)

# Dimensões
betas = []
gammas = []
altura = []

# Roda a simulação para diferentes betas e gammas
for gamma in [x / 10.0 for x in range(1, 11, 1)]:
	ins[2] = gamma
	for beta in [x / 10.0 for x in range(1, 11, 1)]:
		ins[1] = beta

		betas.append(beta)
		gammas.append(gamma)

		# Cálculo da altura
		altura.append(fracz1(nome, model, ins, zvec))

	print(gamma)

# Figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(betas, gammas, altura)

# Legenda
ax.set_xlabel("Beta")
ax.set_ylabel("Gamma")
ax.set_zlabel("Fração das respostas")

# Finalização
path = "Imagens/Plots/"
run = len([ x for x in listdir(path)]) + 1
plt.savefig(path + "TESTE #" + str(run) + ".png")
#plt.show()