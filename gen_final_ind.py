from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
import sys
import os

# Verifica tamanho da entrada
if len(sys.argv) <3:
    print('Modo de Usar: python3 gen_final_ind.py nome_grafo modelo_resposta')
    sys.exit(1)

# Controle para cada modelo_resposta
controles = {
	"Probit": [True, 0, True],
	"Logit": [True, 0, True],
	"Tau-Exposure": [False, 0.5, False],
	"Tau-Exposure-Binario": [False, 0.5, True],
	"Linear": [True, 0, False]
}

# Estimadores para cada modelo_resposta
estimadores = {
	"Probit": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
	"Logit": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
	"Tau-Exposure": ["SUTVA", "Linear", "Tau-Exposure"],
	"Tau-Exposure-Binario": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
	"Linear": ["SUTVA", "Linear", "Tau-Exposure"]
}

# Número correspondente a cada estimador
ests_dict = {
	"SUTVA": 1,
	"Linear": 2,
	"Probit": 3,
	"Logit": 4,
	"Tau-Exposure": 5
}

# Betas utilizados
betas = [
	[0, 0, 1],
	[0, 1, 0.5],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

# Configurações gerais
rodadas = 10
model = 3
estoc_params = [0, 1]

# Parâmetros da geração de dados
nome_grafo = sys.argv[1]
modelo_resposta = sys.argv[2]
modelo_resposta = modelo_resposta if modelo_resposta is not "Logistic" else "Logit"
ins = controles[modelo_resposta]
nomes_estimadores = estimadores[modelo_resposta]
ests = [ests_dict[x] for x in nomes_estimadores]
cores = ['r', 'b', 'g', 'y', 'm', 'c'][:len(nomes_estimadores)]

# Lê o grafo, cria um vetor com randomização individual e o salva
g = Sugar.get_graph(Sugar.path(nome_grafo))
zvec = Sugar.cent(50, g.number_of_nodes())
IO.zvector_to_zfile(zvec, nome_grafo)

# Gera valores
predicoes, ATE = Estimate.multiple_estimate(
	g, zvec, ins, betas, model, ests,
	rodadas, modelo_resposta, estoc_params, True
)

# Escreve valores
pre_path = ["teste", modelo_resposta, nome_grafo]
path = ''

while len(pre_path):
	path += pre_path[0] + '/'
	pre_path.pop(0)
	if not os.path.exists(path):
		os.makedirs(path)

IO.write_results(
	ATE, predicoes, betas, nomes_estimadores,
	path, nome_grafo
)

print("{} - {}: Concluído".format(nome_grafo, modelo_resposta))