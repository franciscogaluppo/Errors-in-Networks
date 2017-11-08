import numpy as np
import networkx as nx
import funcs as f

nome = "p2p-Gnutella08"
g = f.get_graph(nome)
N = g.number_of_nodes()

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
new = bool(int(input("\nNovos parâmetros?\n> ")))
print()

# Entrada de novos parâmetros
if new:
	ins = f.get_input(sim)
	ins_run = f.ins_to_file(ins, nome, sim)

# Seleciona os arquivos de entrada
else:
	ins_run = int(input("Rodada da entrada: "))
	ins = f.file_to_ins(nome, sim, ins_run)

# Escolha do tratamento
new = bool(int(input("\nNovo tratamento?\n> ")))
print()

if new:
	zvector = f.cent(int(input("%z=1: ")), N)
	z_run = f.zvector_to_zfile(zvector, nome)

else:
	z_run = int(input("Rodada do tratamento: "))
	zvector = f.zfile_to_zvector(nome, z_run)

U = np.random.normal(ins[-2], ins[-1], N)

# Roda o modelo
yvector = f.simulate(g, sim, zvector, ins, U)
f.print_out(sim, zvector, yvector)

# Estimadores de ATE
print("\nATE:", f.real_ATE(g, sim, ins, U))
print("SUTVA:", f.ate_estimate(g, zvector, yvector, nome, 1))
print("Linear:", f.ate_estimate(g, zvector, yvector, nome, 2))
if sim != 3 or ins[5] == 1:
	print("Probit:", f.ate_estimate(g, zvector, yvector, nome, 3))

f.yvector_to_yfile(yvector, sim, nome, ins_run, z_run)