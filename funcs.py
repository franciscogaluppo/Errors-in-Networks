from random import random as rd

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1


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

	if out[1] != -1:
		print("Fração de nós com Yi=1 dado que Z=0: {}".format(out[1]))
	else:
		print("Não há nós com Z=0")

	if out[2] != -1:
		print("Fração de nós com Yi=1 dado que Z=1: {}".format(out[2]))
	else:
		print("Não há nós com Z=1")
	

# Recebe entradas do usuário
def get_input(model):
	inputs = []
	inputs.append(float(input("Alpha: ")))

	if model != 1:
		inputs.append(float(input("Beta: ")))
		inputs.append(float(input("Gamma: ")))
		
		if model == 2:
			inputs.append(float(input("Kappa: ")))
		elif model == 3:
			inputs.append(float(input("Tau: ")))
		elif model == 4:
			inputs.append(int(input("Time: ")))
		
	return(inputs)


def comunidade(arq):
	f = open(arq, "r")

	#variaveis para armazenar o numero de elemntos da maior string e essa string
	maior = 0
	string = "1"

	#descobre a linha com maior numero de elementos e armazena em lista
	for line in f:
		if line.count("	") > maior:
			string = line
			maior = line.count("	")

	#remove o \n do final da string
	string = string[:-1]

	#tranforma a string numa lista de strings         
	lista = string.split("	")

	#tranforma as strings em ints
	for i in range(len(lista)):
		lista[i] = int(lista[i])

	return lista


# Cria vetor com porcentagem desejada de z=1
def cent(val, N):
	treatment = []
	for i in range(N):
		if rd() < val/100:
			treatment.append(1)
		else:
			treatment.append(0)
	return treatment


# Cria zvector lendo de um arquivo 
def file_to_zvector(name, N):
	treatment = []
	tf = open(trat, "r")
	for i in range(N):
		r = tf.readline()
		treatment.append(int(r[0]))
	tf.close()
	return treatment


# Fração de vértices de z1 em N
def count_z1(vec):
	out = 0
	N = len(vec)
	for i in range(N):
		out += vec[i]
	return(out/N)


# Fração de vértives de z1 que foram y1
def count_y1z1(vecz, vecy):
	out = 0
	div = 0
	N = len(vecz)
	for i in range(N):
		if(vecz[i] == 1):
			out += vecy[i]
			div += 1

	if div != 0:
		return(out/div)
	return(-1)


# Fração de vértives de z0 que foram y1
def count_y1z0(vecz, vecy):
	out = 0
	div = 0
	N = len(vecz)
	for i in range(N):
		if(vecz[i] == 0):
			out += vecy[i]
			div += 1

	if div != 0:
		return(out/div)
	return(-1)