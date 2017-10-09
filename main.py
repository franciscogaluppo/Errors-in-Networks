from Modelos.resp_based import resp
from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac

import networkx as nx
import funcs as f


nome = "email-Eu-core"
arq = f.path(nome)
g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
ins = f.file_to_ins(nome, sim, 1)
zvector = f.zfile_to_zvector(nome, 2)

# Roda a simulação
if sim == 1:
	yvector = itr(g, ins, zvector)
elif sim == 2:
	yvector = num(g, ins, zvector)
elif sim == 3:
	yvector = frac(g, ins, zvector)
elif sim == 4:
	yvector = resp(g, ins, zvector)

f.print_out(sim, zvector, yvector)

# ATE de fato de FRAC
# y1 = sum(frac(g, ins, f.cent(100, N), 1))
# y0 = sum(frac(g, ins, f.cent(0, N), True))
# print("\nATE:", (y1-y0)/N)

# Estimadores de ATE
print("SUTVA:", f.ate_estimate(zvector, yvector, g, 1))
print("Linear:", f.ate_estimate(zvector, yvector, g, 2))