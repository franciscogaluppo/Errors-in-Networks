#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
import os
import numpy as np
from Funcs.Sugar import int_to_str
from Funcs.Sugar import a

# Imprime os resultados
def print_out(model, zvec, yvec):

    out = [count_z1(yvec), count_y1z0(zvec, yvec), count_y1z1(zvec, yvec)]

    # Imprime o nome do modelo
    if model == 1:
        print("\n--ITR")
    elif model == 2:
        print("\n--Números")
    elif model == 3:
        print("\n--Fração")
    elif model == 4:
        print("\n--Response Based")

    # Imprime os resultados
    print("Fração de nós com Yi=1: {}".format(out[0]))

    if out[1] != None:
        print("Fração de nós com Yi=1 dado que Z=0: {}".format(out[1]))
    else:
        print("Não há nós com Z=0")

    if out[2] != None:
        print("Fração de nós com Yi=1 dado que Z=1: {}".format(out[2]))
    else:
        print("Não há nós com Z=1")


# Recebe o vetor beta do usuário
def get_beta_vector(model):
    betas = []
    betas.append(np.float64(input("Alpha: ")))

    # NOT ITR
    if model != 1:
        betas.append(np.float64(input("Beta: ")))
        betas.append(np.float64(input("Gamma: ")))

    return(betas)


# Recebe os controles
def get_input(model):
    inputs = []
    if model == 2:
        inputs.append(np.float64(input("Kappa: ")))

    elif model == 3:
        inputs.append(bool(int(input("Linear: "))))
        inputs.append(0)
        inputs.append(bool(int(input("Função a: "))))

        if inputs[0] == False:
            inputs[1] = (np.float64(input("Tau: ")))

    elif model == 4:
        inputs.append(int(input("Time: ")))

    return(inputs)


# Pede para o usuário os parámetros da Normal
def get_normal_params():
    params = []
    params.append(np.float64(input("µ: ")))
    params.append(np.float64(input("σ²: ")))
    return(params)


# Fração de vértices de z1 em N
def count_z1(vec):
    out = 0
    N = len(vec)

    for i in range(N):
        out += a(vec[i])
    return(out/N)


# Fração de vértives de z1 que foram y1
def count_y1z1(vecz, vecy):
    out = 0
    div = 0
    N = len(vecz)

    for i in range(N):
        if(vecz[i] == 1):
            out += a(vecy[i])
            div += 1

    if div != 0:
        return(out/div)
    return(None)


# Fração de vértives de z0 que foram y1
def count_y1z0(vecz, vecy):
    out = 0
    div = 0
    N = len(vecz)

    for i in range(N):
        if(vecz[i] == 0):
            out += a(vecy[i])
            div += 1

    if div != 0:
        return(out/div)
    return(None)


# Cria o arquivo do zvector
def zvector_to_zfile(vec, name):
    N = len(vec)
    path = "Datasets/" + name + "/Tratamentos/"
    run = len(listdir(path)) + 1

    # Zero à esquerda
    run = int_to_str(run)

    path += "Z-#" + run + ".txt"
    arq = open(path, "w")

    # Escreve no arquivo
    for i in range(N):
        arq.write("{}\n".format(vec[i]))
    arq.close()

    return(int(run))


# Cria zvector lendo de um arquivo
def zfile_to_zvector(name, run):
    treatment = []

    # Zero à esquerda
    run = int_to_str(run)

<<<<<<< HEAD:src/IO.py
    if not os.path.exists("Datasets/{}/Tratamentos/".format(name)):
        os.makedirs("Datasets/{}/Tratamentos/".format(name))

=======
>>>>>>> eff5402e3aaae873763caff984638436d93aedbf:Funcs/IO.py
    path = "Datasets/" + name + "/Tratamentos/Z-#" + run + ".txt"
    tf = open(path, "r")

    # Lê o arquivo
    for i in tf:
        treatment.append(int(i[0]))

    tf.close()
    return(np.array(treatment))


# Cria o arquivo do ins
def beta_vector_to_file(beta_vector, name, model):
    N = len(beta_vector)
    path = "Datasets/" + name + "/Betas/"
    run = len([ x for x in listdir(path) if ("m" +  str(model)) in x ]) + 1

    # Zero à esquerda
    run = int_to_str(run)

    path += "Beta-m" + str(model) + "|#" + run + ".txt"
    arq = open(path, "w")

    # Escreve no arquivo
    for i in range(N):
        arq.write("{}\n".format(beta_vector[i]))
    arq.close()

    return(int(run))


# Cria ins lendo de um arquivo
def file_to_beta_vector(name, model, run):
    beta_vector = []

    # Zero à esquerda
    run = int_to_str(run)

    path = "Datasets/" + name + "/Betas/Beta-m" + str(model) + "|#" + run + ".txt"
    tf = open(path, "r")

    # Lê o arquivo
    for i in tf:
        if i[0] is "T":
            beta_vector.append(bool(1))
        elif i[0] is "F":
            beta_vector.append(bool(0))
        elif model is 4 and "." not in i:
            beta_vector.append(int(i))
        else:
            beta_vector.append(np.float64(i))
    tf.close()

    return(beta_vector)


# Cria o arquivo do ins
def ins_to_file(ins, name, model):
    if model == 1:
        return(-1)

    N = len(ins)
    path = "Datasets/" + name + "/Ins/"
    run = len([ x for x in listdir(path) if ("m" +  str(model)) in x ]) + 1

    # Zero à esquerda
    run = int_to_str(run)

    path += "ins-m" + str(model) + "|#" + run + ".txt"
    arq = open(path, "w")

    # Escreve no arquivo
    for i in range(N):
        arq.write("{}\n".format(ins[i]))
    arq.close()

    return(int(run))


# Cria ins lendo de um arquivo
def file_to_ins(name, model, run):
    ins = []

    # Zero à esquerda
    run = int_to_str(run)

    path = "Datasets/" + name + "/Ins/ins-m" + str(model) + "|#" + run + ".txt"
    tf = open(path, "r")

    # Lê o arquivo
    for i in tf:
        if i[0] is "T":
            ins.append(bool(1))
        elif i[0] is "F":
            ins.append(bool(0))
        elif model is 4 and "." not in i:
            ins.append(int(i))
        else:
            ins.append(np.float64(i))
    tf.close()

    return(ins)


# Cria o arquivo resposta
def yvector_to_yfile(vec, modelo, name, ins_run, zvec_run, beta_run):
    N = len(vec)
    path = "Datasets/" + name + "/Respostas/"
    zvec_run = int_to_str(zvec_run)
    ins_run = int_to_str(ins_run)
    beta_run = int_to_str(beta_run)

    run = len([ x for x in listdir(path) if ("m" +  str(modelo)) in x
    and ("Z#" + zvec_run) in x and ("ins#" + ins_run) in x]) + 1

    run = int_to_str(run)

    path += "Y-m" + str(modelo) + "|Z#" + zvec_run + "|ins#" + ins_run + "|beta#" + beta_run + "|#" + run + ".txt"
    arq = open(path, "w")

    # Escreve no arquivo
    for i in range(N):
        arq.write("{}\n".format(vec[i]))
    arq.close()

    return(int(run))


# Criva o yvector a partir de um arquivo de resposta
def yfile_to_yvector(name, yvec_run, modelo, ins_run, zvec_run):
    vec = []

    # Zero à esquerda
    yvec_run = int_to_str(yvec_run)
    zvec_run = int_to_str(zvec_run)
    ins_run = int_to_str(ins_run)

    path = "Datasets/" + name + "/Respostas/Y-m" + str(modelo) + "|Z#" + zvec_run + "|ins#" + ins_run + "|beta#" + beta_run + "|#" + yvec_run + ".txt"
    tf = open(path, "r")

    # Lê o arquivo
    for i in tf:
        vec.append(np.float64(i))
    tf.close()
    return(vec)


# Transforma o grafo em dois vetores, um do tratamento e outro das frações
def ZF_file(grafo, zvector, nome):
    N = len(zvector)
    arq = open(nome, "w")

    # Vetor de frações
    frac = []
    for i in range(N):
        soma = np.float64(0)
        for k in grafo.neighbors(i):
            soma += np.float64(zvector[k])
        frac.append(soma/grafo.degree(i))
    frac = np.array(frac)

    # Escreve no arquivo
    for i in range(N):
        arq.write("{} {}\n".format(zvector[i], frac[i]))
    arq.close()


# Gera o arquivo com os resultados
def write_results(ATE, predicoes, betas, nomes_modelos, path="Vals hists/", nome_grafo="email-Eu-core"):
    ests, bet_len, rodadas = predicoes.shape
    cor = 'r'

    for i in range(ests):
        modelo = nomes_modelos[i]

        for j in range(bet_len):
            beta = betas[j]

            arq = open(path + modelo + " " + nome_grafo + " " + str(beta) + ".txt", "w")
            arq.write("ATE real, ATE estimado\n")

            for k in range(rodadas):
                arq.write("{}, {}\n".format(ATE[i][j][k], predicoes[i][j][k]))
            arq.close()   
