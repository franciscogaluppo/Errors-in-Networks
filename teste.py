# Teste da entrada por arquivo

from Modelos.ITR import itr
from Modelos.numero import num
from Modelos.fracao import frac
from Modelos.resp_based import resp

from funcs import get_input as gt
from funcs import print_out as po

ins = gt(3)

po(3, frac(ins, "zeta.txt"))