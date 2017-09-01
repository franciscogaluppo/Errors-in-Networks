import ITR
import numero
import fracao
import resp_based


# Fiquei na dúvida se as entradas são análogas ou não

# Número (menos o kappa)
# arq = raw_input("Arquivo: ")
# alpha = float(input("Alpha: "))
# beta = float(input("Beta: "))
# gama = float(input("Gama: "))

# Fração (menos o tau)
# arq = input("Arquivo: ")
# alpha = float(input("Alpha: "))
# beta = float(input("Beta: "))
# gama = float(input("Gama: "))
# porcentagem = float(input("Porcentagem: "))

# Entradas - Como vão ficar?
arq = input("Arquivo: ")
alpha = float(input("Alpha: "))
beta = float(input("Beta: "))
gama = float(input("Gama: "))
kappa = float(input("Kappa: "))
tau = float(input("Tau: "))
cent = int(input("%z=0: "))
ite = int(input("Ite: "))
T = int(input("T: "))

ITR.itr(arq, beta, ite, cent)
numero.init(arq, alpha, beta, gama, kappa, cent)
fracao.init(arq, alpha, beta, gama, tau, cent)
resp_based.resp_based(arq, alpha, beta, gama, cent, T)