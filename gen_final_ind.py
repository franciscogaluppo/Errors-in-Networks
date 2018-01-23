from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
from Funcs import Manipulate

nomes = [
	"email-Enron",
	"soc-sign-bitcoinotc",
	"soc-sign-epinions",
	"Wiki-Vote"
]

rodadas = 1000
model = 3
ins = [True, 0, True]
media = 0
var = 1

betas = [
	[0, 0, 1],
	[0, 0.5, 1],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

cores = ['r', 'b', 'g', 'y', 'm', 'c']
ests = [x+1 for x in range(5)]
nomes_modelo = ["SUTVA", "Linear", "Probit", "Logit", "Média C1 C0", "Linear C1 C0"]

# Grafo
for nome_grafo in nomes:
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
		"Resultados/Valores Finais/" + nome_grafo + '/',
		nome_grafo
	)

	Manipulate.hist(
		predicoes, ATE, betas, 50, nomes_modelo,
		"Imagens/Histogramas Finais/" + nome_grafo + '/',
		nome_grafo, cores
	)

	print(nome_grafo + " concluído")
