# Funções que importam os módulos

from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac
from Modelos.resp_based import resp

# Função do Average Treatment Effect
def ate(ins, model, Za=-1, Zb=-1, comu=-1):

	# ITR
	if model == 1:
		val1 = itr(ins, -1, comu)

	# Número
	elif model == 2:
		val1 = num(ins, -1, comu)

	# Fração
	elif model == 3:
		val1 = frac(ins, -1, comu)

	# Response Based
	elif model == 4:
		val1 = resp(ins, -1, comu)

	return(val1[0] - val2[0])