from os import system
import numpy as np

for sig_sqd in [x / np.float64(10.0) for x in range(1, 11, 1)]:
	system("python3 plots.py 0 {}".format(sig_sqd))
	print(str(int(sig_sqd*100)) + "%")