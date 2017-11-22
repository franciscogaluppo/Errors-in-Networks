import funcs as f
import numpy as np

nome = "email-Eu-core"	  # Nome do Dataset
g = f.get_graph(nome)     # Grafo
rodadas = 1000            # Número de rodadas
trat = 1		  	      # Número do vetor de tratamento
model = 3		          # Número do modelo da simulação
beta = [0, 1, 1]          # Vetor Beta
ins = [True, 0, False]    # Linear (True) e não Binário (False)

N = g.number_of_nodes()
zvec = f.zfile_to_zvector(nome, trat)

media = 0                 # Média da distribuição Normal
var = 1                   # Variância da distribuição Normal

est_model = 2
predicoes = np.empty(rodadas)
ATE = np.empty(rodadas)

for i in range(rodadas):
	U = np.random.normal(media, var, N)

	yvec = f.simulate(g, model, zvec, beta, ins, U)
	predicoes[i] = f.ate_estimate(g, zvec, yvec, est_model)
	ATE[i] = f.real_ATE(g, model, beta, ins, U)

mse = ((predicoes - ATE) ** 2).mean()
print(mse)