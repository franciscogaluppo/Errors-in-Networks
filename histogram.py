from sys import argv
import funcs as f
from Modelos.fracao import frac

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from sklearn import linear_model
from statsmodels.discrete.discrete_model import Probit
from statsmodels.discrete.discrete_model import Logit


nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = int(argv[1])    # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação

betas = [[0, 0, 1], [0, 0.5, 0.5], [0, 1, 0], [0, 1, 1], [0, 1, 2]]
cores = ['r', 'b', 'g', 'y', 'm']
ests = [2, 3, 4]
nomes_modelo = ["Linear Binário", "Probit", "Logit"]

ins = [True, 0, True]     # Linear (True) e Binário (True)

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal

# Vetor tau
tau = []
for i in range(N):
	soma = 0.0
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

predicoes = np.empty(shape=(len(ests), len(betas), rodadas))
ATE = np.empty(shape=(len(ests), len(betas), rodadas))

# Gera os dados e coloca num array
for i in range(len(ests)):
	est_model = ests[i]

	for j in range(len(betas)):
		beta = betas[j]
		
		# Estima
		for k in range(rodadas):
			U = np.random.normal(media, var, N)
			yvec = frac(g, beta, ins, zvec, U)
			
			# Linear
			if est_model == 2:
				lr = linear_model.LinearRegression().fit(features, yvec).coef_
				predicoes[i][j][k] = (lr[1] + lr[2])

			# Probit
			if est_model == 3:
				vals = Probit(yvec, features).fit(disp=0).params
				predicoes[i][j][k] = (norm.cdf(sum(vals)) - norm.cdf(vals[0]))

			# Logit
			if est_model == 4:
				vals = Logit(yvec, features).fit(disp=0).params
				predicoes[i][j][k] = (
					(np.exp(-vals[0]) - np.exp(-sum(vals)))/
					((1 + np.exp(-vals[0])) * (1 + np.exp(-sum(vals))))
				)

			ATE[i][j][k] = f.real_ATE(g, model, beta, ins, U)

			print("est: {}/{}| beta: {}/{}| rodada: {}/{}".format(i+1, 3, j+1, 5, k+1, rodadas))

print("Criando os gráficos")

# Cria as saídas
for i in range(len(ests)):
	nome_do_modelo = nomes_modelo[i]

	for j in range(len(betas)):
		cor = cores[j]
		beta = betas[j]
		
		# Cálculo de valores
		ATE_est = predicoes[i][j].mean()
		ATE_real = ATE[i][j].mean()
		erro = (predicoes[i][j] - ATE[i][j]).mean()
		var = predicoes[i][j].var()

		# Histograma
		fig, ax = plt.subplots() 
		plt.xlabel("ATE estimado")
		plt.ylabel("Número de aparições")
		n, bins, patches = ax.hist(predicoes[i][j], bins=50, histtype='bar')
		plt.axvline(ATE_real, color='black', linestyle='dashed', linewidth=2)

		# cores
		for patch in patches:
			patch.set_facecolor(cor)

		# Legenda
		vals = "Média do ATE estimado: {}\nMédia do ATE real: {}\nErro Médio: {}\nVariância: {}\n".format(ATE_est, ATE_real, erro, var)
		handles, labels = ax.get_legend_handles_labels()
		handles.append(mpatches.Patch(color='none', label=vals))
		plt.legend(handles=handles, fontsize=6)

		# Gera o gráfico
		plt.title('Estimativas do ATE — Email ' + str(beta) + " " + nome_do_modelo)
		plt.savefig("Imagens/Histogramas/" + nome_do_modelo + "/Histograma Email " + str(beta) + " " + nome_do_modelo + " .png")

		# Gera o arquivo com os resultados
		arq = open("Vals hists/Email " + str(beta) + " " + nome_do_modelo + ".txt", "w")
		arq.write("ATE real, ATE estimado\n")

		for k in range(rodadas):
			arq.write("{}, {}\n".format(ATE[i][j][k], predicoes[i][j][k]))
		arq.close()	