# Importa os modelos
from ITR import itr
from numero import init as num
from fracao import init as frac
from resp_based import resp_based as resp

# Importa as funções
from funcs import print_out as po
from funcs import get_input as gt

# Seleciona o modelo
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
print("")

# Recebe as entradas
ins = gt(sim)

# Chama o modelo
if sim == 1:
	po(sim, itr(ins))

elif sim == 2:
	po(sim, num(ins))

elif sim == 3:
	po(sim, frac(ins))

elif sim == 4:
	po(sim, resp(ins))