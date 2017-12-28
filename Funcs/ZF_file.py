from sys import argv
from funcs import get_graph
from funcs import ZF_file as zf
from funcs import zfile_to_zvector as ztz

# Entrada
nome = argv[1]
zvec_run = int(argv[2])

# Acha o grafo e seu tratamento
g = get_graph(nome)
zvector = ztz(nome, zvec_run)

# Cria a saida
nome = "ZF/" + nome + "_ZF.txt"
zf(g, zvector, nome)
print("Pronto!")