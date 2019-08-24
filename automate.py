from sys import argv
import re
import numpy as np

arq = open(argv[1], 'r')
grafo_dict = dict()
grafo, beta, modelo = [0,0,0]
resp = argv[1].split("/")[1].split(".")[0]

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

binaridade = {
        "Logit":True,
        "Probit":True,
        "Tau-Exposure-Binario":True,
        "Tau-Exposure":False,
        "Linear":False
}

binario = binaridade[resp]

nomes_modelo = [
        "SUTVA",
        "Logit",
        "Probit",
        "Tau-Exposure"
] if binario else [
        "SUTVA",
        "Linear",
        "Tau-Exposure"
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

        if binario:
            print("""
\\begin{{table}}[!t]
        \\centering
        %\\label{{}}
        \\begin{{tabular}}{{|l||*{{5}}{{c|}}}}\\hline
                \\multirow{{3}}{{*}}{{Estimador}} & \\multicolumn{{5}}{{|c|}}{{Vetor de parâmetros $\\bbeta$ e $\\text{{ATE}}_\\text{{logistic}}$}}\\\\ \\cline{{2-6}}
                &$(0,0,1)$ & $(0,1,0.5)$& $(0,1,0)$ & $(0,1,1)$ & $(0,1,2)$\\\\
                & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ \\\\ \\hline \\hline
                SUTVA                 &{}&{}&{}&{}&{}\\\\\\hline
                Logistic              &{}&{}&{}&{}&{}\\\\\\hline
                Probit                &{}&{}&{}&{}&{}\\\\\\hline
                $\\tau$-Exposure      &{}&{}&{}&{}&{}\\\\\\hline
        \\end{{tabular}}
        \\caption{{"MSE dos ATE estimados para o modelo de resposta {} na rede {}"}}
\\end{{table}}""".format(*lista, resp, g))
        
        else:
            print("""
\\begin{{table}}[!t]
        \\centering
        %\\label{{}}
        \\begin{{tabular}}{{|l||*{{5}}{{c|}}}}\\hline
                \\multirow{{3}}{{*}}{{Estimador}} & \\multicolumn{{5}}{{|c|}}{{Vetor de parâmetros $\\bbeta$ e $\\text{{ATE}}_\\text{{logistic}}$}}\\\\ \\cline{{2-6}}
                &$(0,0,1)$ & $(0,1,0.5)$& $(0,1,0)$ & $(0,1,1)$ & $(0,1,2)$\\\\
                & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ & $\\text{{ATE}} = $ \\\\ \\hline \\hline

                SUTVA                 &{}&{}&{}&{}&{}\\\\\\hline
                Linear                &{}&{}&{}&{}&{}\\\\\\hline
                $\\tau$-Exposure      &{}&{}&{}&{}&{}\\\\\\hline
        \\end{{tabular}}
        \\caption{{"MSE dos ATE estimados para o modelo de resposta {} na rede {}"}}
\\end{{table}}""".format(*lista, resp, g))
