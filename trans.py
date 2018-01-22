from sys import argv
from os import system
import re

arq = open("set.txt", "r")
out = open(".out", "w")

for i in arq:
	string = re.split("\s|,", i)
	out.write("{} {}\n".format(string[0], string[1]))
arq.close()
out.close()

system("mv .out set.txt")