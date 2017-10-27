#!/usr/bin/env python
# -*- coding: utf-8 -*-

import funcs as f
import matplotlib.pyplot as plt

nome = "p2p-Gnutella08"
ins = [-1, 1, 1, 0, 0, 1]
zvec = f.zfile_to_zvector(nome, 2)

x = list()
y = list()

for i in range(100):
	ins[3] = i

	y.append(f.real_ATE(4, ins, nome) - f.ate_estimate(zvec, f.simulate(4, zvec, ins, nome), nome, 2))
	x.append(i)

	print("Rodada:", i, "—", y[i])

plt.scatter(x, y)
plt.show()
