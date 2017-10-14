import networkx as nx
import funcs as f

nome = "email-Eu-core"

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n> "))
new = bool(int(input("\nNovos parâmetros?\n> ")))
print()

# Entrada de novos parâmetros
if new:
	ins = f.get_input(sim)
	ins_run = f.ins_to_file(ins, nome, sim)

	g = nx.read_edgelist(f.path(nome), nodetype=int)
	N = g.number_of_nodes()
	zvector = f.cent(int(input("%z=1: ")), N)
	z_run = f.zvector_to_zfile(zvector, nome)

# Seleciona os arquivos de entrada
else:
	ins_run = int(input("Rodada da entrada: "))
	ins = f.file_to_ins(nome, sim, ins_run)
	
	z_run = int(input("Rodada do tratamento: "))
	zvector = f.zfile_to_zvector(nome, z_run)


# Roda o modelo
yvector = f.simulate(sim, zvector, ins, nome)
f.print_out(sim, zvector, yvector)

# Estimadores de ATE
print("\nATE:", f.real_ATE(sim, ins, nome))
print("SUTVA:", f.ate_estimate(zvector, yvector, nome, 1))
print("Linear:", f.ate_estimate(zvector, yvector, nome, 2))

f.yvector_to_yfile(yvector, sim, nome, ins_run, z_run)