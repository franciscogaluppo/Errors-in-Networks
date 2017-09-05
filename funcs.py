# Função a
def a(valor):
	if valor <= 0: return 0
	return 1

# Imprime os resultados
def print_out(model, out):
	if model > 1 and model <= 4:

		# Imprime o nome do modelo
		if model == 2:
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
	
	# Imprime para o ITR, apresenta mais valores
	elif model == 1:
		print("\n--ITR")
		print("Fração de nós com Yi=1: {} ± {}".format(out[0], out[1]))
		
		if out[1] != -1:
			print("Fração de nós com Yi=1 dado que Z=0: {} ± {}".format(out[2], out[3]))
		else:
			print("Não há nós com Z=0")

		if out[4] != -1:
			print("Fração de nós com Yi=1 dado que Z=1: {} ± {}".format(out[4], out[5]))
		else:
			print("Não há nós com Z=1")
	return


# Recebe entradas do usuário
def get_input(model):

	# Entrada de arq e alpha
	inputs = []
	inputs.append(input("Arquivo: "))
	inputs.append(float(input("Alpha: ")))

	# Entrada de beta, gama, kappa e tau
	if model != 1:
		inputs.append(float(input("Beta: ")))
		inputs.append(float(input("Gamma: ")))
		
		if model == 2:
			inputs.append(float(input("Kappa: ")))
		elif model == 3:
			inputs.append(float(input("Tau: ")))

	# Entrada da porcentagem
	inputs.append(float(input("%z=0: ")))

	# Entrada de ite e T
	if model == 1:
		inputs.append(int(input("Ite: ")))
	elif model == 4:
		inputs.append(int(input("T: ")))

	return(inputs)