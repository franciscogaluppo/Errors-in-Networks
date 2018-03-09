from Funcs import Manipulate
import numpy as np
import re
import teste

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
# Modelo_gerador = "Probit"
Modelo_gerador = "Tau-Exposure"
cores = ['r', 'b', 'g', 'y', 'm']

for j in range(len(nomes_modelo)):
	for k in range(len(betas)):
		grafo = list()
		for i in range(len(nomes)):
			predicoes = np.empty(shape=(num_rodadas))
			ATE = np.empty(shape=(num_rodadas))

			arq = open("Resultados/Valores Finais/{0}/{1}/{2} {1} {3}.txt".format(
				Modelo_gerador, nomes[i], nomes_modelo[j], betas[k]), "r")
			
			m = 0
			for l in arq:
				vals = [float(x) for x in re.split("\s|,", l) if x not in ["ATE", "real", "estimado", ""]] 
				if vals == []:
					continue
				ATE[m], predicoes[m] = vals
				m += 1
			arq.close()

			grafo.append([ATE, predicoes])

		teste.mult_hist(grafo, nomes, nomes_modelo[j], Modelo_gerador, betas[k], 50, "Imagens/Histogramas Finais/{}/Todos/".format(Modelo_gerador), cores[k])