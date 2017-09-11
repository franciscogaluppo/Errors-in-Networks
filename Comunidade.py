def comunidade(arq):
	f = open(arq, "r")

	maior = 0						#variaveis para armazenar o numero de elemntos da maior string e essa string
	string = "1"

	for line in f:                  #descobre a linha com maior numero de elementos e armazena em lista
		if line.count("	") > maior:
			string = line
			maior = line.count("	")

	string = string[:-1]            #remove o \n do final da string
	lista = string.split("	")      #tranforma a string numa lista de strings

	for i in range(len(lista)):     #tranforma as strings em ints
		lista[i] = int(lista[i])

	return lista