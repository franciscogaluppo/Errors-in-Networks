from sys import argv
import re
import numpy as np

arq = open(argv[1], 'r')
grafo_dict = dict()
grafo, beta, modelo = [0,0,0]

for line in arq:
	quebra = line.replace(" - ", "!").split("!")
	
	if quebra[0] is '\n':
		continue

	elif quebra[0][0] is "M":
		quebra = quebra[0].split()
		grafo_dict[grafo][beta][modelo] = np.float64(quebra[1])

	else:
		grafo, beta, modelo = [x for x in quebra if x is not "-"]
		modelo = modelo.replace("\n", "")
		beta = str([np.float64(x) for x in re.split("\[|\]|,", beta) if len(x) <= 4 and x is not ''])
		if grafo not in grafo_dict:
			grafo_dict[grafo] = dict()
		if beta not in grafo_dict[grafo]:
			grafo_dict[grafo][beta] = dict()


# print(grafo_dict)

nomes_modelo = [
	"Linear",
	"Logit",
	"Média C1 C0",
	"Probit",
	"SUTVA"
]

betas = [
	[0.0, 0.0, 1.0],
	[0.0, 1.0, 0.5],
	[0.0, 1.0, 0.0],
	[0.0, 1.0, 1.0],
	[0.0, 1.0, 2.0]
]

for g in grafo_dict: 
	lista = []
	for modelo in nomes_modelo:
		for beta in betas:
			lista.append(grafo_dict[g][str(beta)][modelo])

	lista = ["{:.5f}".format(x) for x in lista]

	print("""
%{}{}
\\begin{{table}}[h]
	\\centering
	%\\label{{}}
	\\begin{{tabular}}{{|l||*{{5}}{{c|}}}}\\hline
		\\backslashbox{{Estimador}}{{Vetor $\\beta$}}
		&\\makebox[3em]{{$(0,0,1)$}}&\\makebox[3em]{{$(0,1,0.5)$}}&\\makebox[3em]{{$(0,1,0)$}}
		&\\makebox[3em]{{$(0,1,1)$}}&\\makebox[3em]{{$(0,1,2)$}}\\\\\\hline\\hline
		Linear      &{}&{}&{}&{}&{}\\\\\\hline
		Logistic    &{}&{}&{}&{}&{}\\\\\\hline
		Média C1 C0 &{}&{}&{}&{}&{}\\\\\\hline
		Probit      &{}&{}&{}&{}&{}\\\\\\hline
		SUTVA       &{}&{}&{}&{}&{}\\\\\\hline
	\\end{{tabular}}
\\end{{table}}

""".format(g, " Tau-Exposure", *lista))
		