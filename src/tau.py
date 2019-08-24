from Funcs.IO import zfile_to_zvector as ler
from Funcs.Sugar import get_graph as gg
from Funcs.Sugar import path as p
from scipy.stats import norm
import numpy as np

def leitura(nome, numero):
    z = ler(nome, numero) 
    n = len(z)
    f = np.empty(shape=(n))
    g = gg(p(nome))

    for i in range(n):
        soma = np.float64(0)
        for j in g.neighbors(i):
            soma += np.float64(z[j])
        f[i] = soma/g.degree(i)
    
    return([z, f])

def calctau(z, f, tau):
    c1, c0 = [0, 0]

    for i in range(len(z)):
        if z[i] == 1 and f[i] >= tau:
            c1 += 1
        elif z[i] == 0 and f[i] <= 1 - tau:
            c0 += 1

    return(1/c1 + 1/c0)

def calctau_bin(z, f, tau, beta):
    c1, c0 = [0, 0]

    for i in range(len(z)):
        if z[i] == 1 and f[i] >= tau:
            c1 += 1
        elif z[i] == 0 and f[i] <= 1 - tau:
            c0 += 1

    return((norm.cdf(beta[0]+beta[1])*(1-norm.cdf(beta[0]+beta[1])))/c1 + ((norm.cdf(beta[0])*(1-norm.cdf(beta[0]))))/c0)

