import numpy as np
import networkx as nx
import funcs as f

nome = "email-Eu-core"
g = f.get_graph(nome)
N = g.number_of_nodes()

# Entradas
sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
new = bool(int(input("Novo vetor beta? ")))

# Entrada de novos betas
if new:
    beta_vector = f.get_beta_vector(sim)
    beta_run = f.beta_vector_to_file(beta_vector, nome, sim)

# Seleciona os arquivos de beta
else:
    beta_run = int(input("Rodada do beta: "))
    beta_vector = f.file_to_beta_vector(nome, sim, beta_run)

ins = []
ins_run = 0

if sim != 1:
    new == bool(int(input("Novos controles? ")))

    # Entrada de novos controles
    if new:
        ins = f.get_input(sim)
        ins_run = f.ins_to_file(ins, nome, sim)

    # Seleciona os arquivos de controle
    else:
        ins_run = int(input("Rodada da entrada: "))
        ins = f.file_to_ins(nome, sim, ins_run)



new = bool(int(input("Novo tratamento? ")))

# Tratamento novo aleatório
if new:
    zvector = f.cent(int(input("%z=1: ")), N)
    z_run = f.zvector_to_zfile(zvector, nome)

# Escolha do tratamento
else:
    z_run = int(input("Rodada do tratamento: "))
    zvector = f.zfile_to_zvector(nome, z_run)

normal = f.get_normal_params()
U = np.random.normal(normal[0], normal[1], N)

# Roda o modelo
yvector = f.simulate(g, sim, zvector, beta_vector, ins, U)
f.print_out(sim, zvector, yvector)

# Estimadores de ATE
print("\nATE:        ", f.real_ATE(g, sim, beta_vector, ins, U))
print("SUTVA:      ", f.ate_estimate(g, zvector, yvector, 1))
print("Linear:     ", f.ate_estimate(g, zvector, yvector, 2))
if not(sim == 3 and ins[0]):
    print("Probit:     ", f.ate_estimate(g, zvector, yvector, 3))
    print("Logit:      ", f.ate_estimate(g, zvector, yvector, 4))
    print("Variância:  ", f.var_linear(g, zvector, yvector, beta_vector))

f.yvector_to_yfile(yvector, sim, nome, ins_run, z_run, beta_run)
