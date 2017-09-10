# Teste da entrada por arquivo

from Modelos.resp_based import resp_based as resp
from funcs import get_input as gt
from funcs import print_out as po

ins = gt(4)

po(4, resp(ins, "zeta.txt"))