import networkx as nx
import funcs as f

nome = "email-Eu-core"

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
ins_run = 1
z_run = 2

ins = f.file_to_ins(nome, sim, ins_run)
# ------- OPCIONAL
# ins = f.get_input(sim)
# f.ins_to_file(ins, nome, sim)

zvector = f.zfile_to_zvector(nome, z_run)
# ------- OPCIONAL
# g = nx.read_edgelist(path(name), nodetype=int)
# N = g.number_of_nodes()
# zvector = f.cent(int(input("%z=1: ")), N)

yvector = f.simulate(sim, zvector, ins, nome)
f.print_out(sim, zvector, yvector)

# Estimadores de ATE
print("\nATE:", f.real_ATE(sim, ins, nome))
print("SUTVA:", f.ate_estimate(zvector, yvector, nome, 1))
print("Linear:", f.ate_estimate(zvector, yvector, nome, 2))

f.yvector_to_yfile(yvector, sim, nome, ins_run, z_run)