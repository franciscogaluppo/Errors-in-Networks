# Funções que não importam os módulos

# Função a
def a(valor):
	if valor <= 0: return 0
	return 1

# Imprime os resultados
def print_out(model, out):

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

	# Entrada de arq e alpha
	inputs = []
	inputs.append(input("Arquivo: "))
	inputs.append(float(input("Alpha: ")))

	# Entrada de beta, gama, kappa, tau e T
	if model != 1:
		inputs.append(float(input("Beta: ")))
		inputs.append(float(input("Gamma: ")))
		
		# Kappa
		if model == 2:
			inputs.append(float(input("Kappa: ")))
		# Tau
		elif model == 3:
			inputs.append(float(input("Tau: ")))
		# T	
		elif model == 4:
			inputs.append(int(input("T: ")))

	# Entrada de ite
	else:
		inputs.append(int(input("Ite: ")))

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