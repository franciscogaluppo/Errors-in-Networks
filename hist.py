from Funcs import Manipulate
import numpy as np
import re

nomes = [
	"soc-sign-bitcoinotc",
	"email-Enron",
	# "soc-sign-epinions",
	"Wiki-Vote"
]

betas = [
	[0, 0, 1],
	[0, 1, 0.5],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

nomes_modelo = [
	"SUTVA",
	"Linear",
	"Probit",
	"Logit",
	"Média C1 C0"
]

num_rodadas = 1000
# Modelo_gerador = "Tau-Exposure"
Modelo_gerador = "Probit"
cores = ['r', 'b', 'g', 'y', 'm']

predicoes = np.empty(shape=(len(nomes_modelo), len(betas), num_rodadas))
ATE = np.empty(shape=(len(nomes_modelo), len(betas), num_rodadas))

for i in range(len(nomes)):
	for j in range(len(nomes_modelo)):
		for k in range(len(betas)):
			arq = open("Resultados/Valores Finais/{0}/{1}/{2} {1} {3}.txt".format(
				Modelo_gerador, nomes[i], nomes_modelo[j], betas[k]), "r")
			
			m = 0
			for l in arq:
				vals = [float(x) for x in re.split("\s|,", l) if x not in ["ATE", "real", "estimado", ""]] 
				if vals == []:
					continue
				ATE[j][k][m], predicoes[j][k][m] = vals
				m += 1
			arq.close()

	Manipulate.hist(
		predicoes, ATE, betas, 50, nomes_modelo, nomes[i], Modelo_gerador,
		"Imagens/Histogramas Finais/{}/".format(Modelo_gerador) + nomes[i] + '/', cores
	)