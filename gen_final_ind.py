from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
#from Funcs import Manipulate
import sys

if len(sys.argv) < 2:
    print('Incorrect number of arguments.')
    sys.exit(1)

nome_grafo = sys.argv[1]

nomes = [
	"soc-sign-bitcoinotc",
	"email-Enron",
	"soc-sign-epinions",
	"Wiki-Vote"
]

controles = [
	[True, 0, True],
	[False, 0.5, True]
]

rodadas = 1000
model = 3
media = 0
var = 1

betas = [
	[0, 0, 1],
	[0, 1, 0.5],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

cores = ['r', 'b', 'g', 'y', 'm', 'c']
ests = [x+1 for x in range(5)]
nomes_modelo = ["SUTVA", "Linear", "Probit", "Logit", "Média C1 C0"]

# Grafo
for i in range(len(controles)):
	ins = controles[i]

	pasta = "Probit/" if not i else "Tau-Exposure/"

	#for nome_grafo in nomes:
	g = Sugar.get_graph(Sugar.path(nome_grafo))
	zvec = Sugar.cent(50, g.number_of_nodes())
	IO.zvector_to_zfile(zvec, nome_grafo)

	# Valores
	predicoes, ATE = Estimate.multiple_estimate(
		g, zvec, ins, betas, model, ests,
		rodadas, [media, var], True, 0.5
	)

	IO.write_results(
		ATE, predicoes, betas, nomes_modelo,
		"Resultados/Valores Finais/" + pasta + nome_grafo + '/',
		nome_grafo
	)

	#Manipulate.hist(
	#	predicoes, ATE, betas, 50, nomes_modelo,
	#	"Imagens/Histogramas Finais/" + pasta + nome_grafo + '/',
	#	nome_grafo, cores
	#)

	print(nome_grafo + " concluído")
