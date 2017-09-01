import ITR
import numero
import fracao
import resp_based

sim = int(input("[1]ITR\n[2]Número\n[3]Fração\n[4]Response Based\n\n> "))
print("")

if sim == 1:
	arq = input("Arquivo: ")
	alpha = float(input("Alpha: "))
	cent = int(input("%z=0: "))
	ite = int(input("Ite: "))
	ITR.itr(arq, alpha, ite, cent)

elif sim == 2:
	arq = input("Arquivo: ")
	alpha = float(input("Alpha: "))
	beta = float(input("Beta: "))
	gama = float(input("Gama: "))
	kappa = float(input("Kappa: "))
	cent = int(input("%z=0: "))
	numero.init(arq, alpha, beta, gama, kappa, cent)

elif sim == 3:
	arq = input("Arquivo: ")
	alpha = float(input("Alpha: "))
	beta = float(input("Beta: "))
	gama = float(input("Gama: "))
	tau = float(input("Tau: "))
	cent = float(input("%z=0: "))
	fracao.init(arq, alpha, beta, gama, tau, cent)

elif sim == 4:
	arq = input("Arquivo: ")
	alpha = float(input("Alpha: "))
	beta = float(input("Beta: "))
	gama = float(input("Gama: "))
	cent = int(input("%z=0: "))
	T = int(input("T: "))
	resp_based.resp_based(arq, alpha, beta, gama, cent, T)