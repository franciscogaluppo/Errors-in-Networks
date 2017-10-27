#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
