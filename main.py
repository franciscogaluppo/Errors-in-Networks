from Modelos.resp_based import resp
from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac

import networkx as nx
import funcs as f

arq = "set1.txt"

g = nx.read_edgelist(arq, nodetype=int)
N = g.number_of_nodes()

sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
porcentagem = int(input("\n%z=1: "))
ins = f.get_input(sim)

zvector = f.cent(porcentagem, N)

if sim == 1:
	yvector = itr(g, ins, zvector)
elif sim == 4:
	yvector = num(g, ins, zvector)
elif sim == 3:
	yvector = frac(g, ins, zvector)
elif sim == 4:
	yvector = resp(g, ins, zvector)

f.print_out(sim, zvector, yvector)