import numpy as np
import networkx as nx

from Funcs import Sugar
from Funcs import IO
from Funcs import Estimate
from Funcs import Simulate

nome = "email-Eu-core"
g = Sugar.get_graph(Sugar.path(nome))
N = g.number_of_nodes()

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
new = bool(int(input("Novo vetor beta? ")))

# Entrada de novos betas
if new:
    beta_vector = IO.get_beta_vector(sim)
    beta_run = IO.beta_vector_to_file(beta_vector, nome, sim)

# Seleciona os arquivos de beta
else:
    beta_run = int(input("Rodada do beta: "))
    beta_vector = IO.file_to_beta_vector(nome, sim, beta_run)

ins = []
ins_run = 0

if sim != 1:
    new = bool(int(input("Novos controles? ")))

    # Entrada de novos controles
    if new:
        ins = IO.get_input(sim)
        ins_run = IO.ins_to_file(ins, nome, sim)

    # Seleciona os arquivos de controle
    else:
        ins_run = int(input("Rodada da entrada: "))
        ins = IO.file_to_ins(nome, sim, ins_run)



new = bool(int(input("Novo tratamento? ")))

# Tratamento novo aleatório
if new:
    zvector = Sugar.cent(int(input("%z=1: ")), N)
    z_run = IO.zvector_to_zfile(zvector, nome)

# Escolha do tratamento
else:
    z_run = int(input("Rodada do tratamento: "))
    zvector = IO.zfile_to_zvector(nome, z_run)

normal = IO.get_normal_params()
U = np.random.normal(normal[0], normal[1], N)

# Roda o modelo
yvector = Simulate.simulate(g, sim, zvector, beta_vector, ins, U)
IO.print_out(sim, zvector, yvector)

# Estimadores de ATE
print("\nATE:        ", Simulate.real_ATE(g, sim, beta_vector, ins, U))
print("SUTVA:      ", Estimate.estimate(g, zvector, yvector, 1))
print("Linear:     ", Estimate.estimate(g, zvector, yvector, 2))
if not(sim == 3 and not ins[2]):
    print("Probit:     ", Estimate.estimate(g, zvector, yvector, 3))
    print("Logit:      ", Estimate.estimate(g, zvector, yvector, 4))
    print("Variância:  ", Sugar.var_linear(g, zvector, yvector, beta_vector))

IO.yvector_to_yfile(yvector, sim, nome, ins_run, z_run, beta_run)
