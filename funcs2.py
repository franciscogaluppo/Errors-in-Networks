# Funções que importam os módulos

from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac
from Modelos.resp_based import resp

# Função do Average Treatment Effect
def ate(ins, model, Za=-1, Zb=-1, comu=-1):

	# ITR
	if model == 1:
		val1 = itr(ins, Za, comu)
		val2 = itr(ins, Zb, comu)

	# Número
	elif model == 2:
		val1 = num(ins, Za, comu)
		val2 = num(ins, Zb, comu)

	# Fração
	elif model == 3:
		val1 = frac(ins, Za, comu)
		val2 = frac(ins, Zb, comu)

	# Response Based
	elif model == 4:
		val1 = resp(ins, Za, comu)
		val2 = resp(ins, Zb, comu)

	return(val1[0] - val2[0])