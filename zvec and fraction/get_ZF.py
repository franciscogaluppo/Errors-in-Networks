from sys import argv
from Funcs.IO import zfile_to_zvector as ler
from Funcs.IO import ZF_file as out
from Funcs.Sugar import get_graph as gg
from Funcs.Sugar import path as p

nome = argv[1]
run = int(argv[2])
zvec = ler(nome, run)
g = gg(p(nome))
out(g, zvec, "ZF_{}_{}.txt".format(nome, run))
