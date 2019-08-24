import subprocess
import sys

# Verifica tamanho da entrada
if len(sys.argv) <3:
    print('Modo de Usar: python3 p.py nome_grafo modelo_resposta')
    sys.exit(1)

# Estimadores para cada modelo_resposta
estimadores = {
    "Probit": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
    "Logit": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
    "Tau-Exposure": ["SUTVA", "Linear", "Tau-Exposure"],
    "Tau-Exposure-Binario": ["SUTVA", "Probit", "Logit", "Tau-Exposure"],
    "Linear": ["SUTVA", "Linear", "Tau-Exposure"]
}

# Betas utilizados
betas = [
	[0, 0, 1],
	[0, 1, 0.5],
	[0, 1, 0],
	[0, 1, 1],
	[0, 1, 2]
]

grafo = sys.argv[1]
modelo = sys.argv[2]
correto = modelo if modelo != "Tau-Exposure-Binario" else "Tau-Exposure"
pre_cmd = ["Rscript", "./t.R", grafo, modelo, correto]

for beta in betas:
    print(grafo, modelo, beta)
    for est in estimadores[modelo]:
        if est == correto:
            continue
        cmd = pre_cmd + [est, str(beta)]
        p = float(subprocess.check_output(cmd, universal_newlines=True).split()[0])
        print("\t{}: {} x {} -> p = {}".format("Y" if p < 0.05 else "N", correto, est, p))
    print()
