import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
from scipy import stats
from math import sqrt

betas = [
    [0, 0, 1],
    [0, 1, 0.5],
    [0, 1, 0],
    [0, 1, 1],
    [0, 1, 2]
]

redes = ["soc-sign-bitcoinotc", "email-Enron", "Wiki-Vote"]
modelos_resposta = ["Logit", "Probit", "Tau-Exposure-Binario", "Linear", "Tau-Exposure"]
alpha = 0.05

ys = [[[0.00043966, 0.00037938, 0.00044565, 0.00032177, 0.00025223],
		[0.00007595, 0.00006784, 0.00007678, 0.00006017, 0.00005153],
		[0.00041402, 0.00036908, 0.00041847, 0.00032717, 0.00028075]],
		
		[[0.00036779, 0.00029857, 0.00037297, 0.00025912, 0.00026002],
		[0.00006477, 0.00005236, 0.00006599, 0.00004523, 0.00004593],
		[0.00035333, 0.00028243, 0.00035869, 0.00024272, 0.00024605]],

		[[0.00068182, 0.00049890, 0.00049890, 0.00049890, 0.00049890],
		[0.00013376, 0.00010565, 0.00010565, 0.00010565, 0.00010565],
		[0.00069477, 0.00051606, 0.00051606, 0.00051606, 0.00051606]],

		[[0.0019763, 0.0019763, 0.0019763, 0.0019763, 0.0019763],
		[0.00034176, 0.00034176, 0.00034176, 0.00034176, 0.00034176],
		[0.0018539, 0.0018539, 0.0018539, 0.0018539, 0.0018539]],

		[[0.00272727, 0.00272727, 0.00272727, 0.00272727, 0.00272727],
		[0.00053503, 0.00053503, 0.00053503, 0.00053503, 0.00053503],
		[0.00277907, 0.00277907, 0.00277907, 0.00277907, 0.00277907]]]

path = lambda w, x, y, z: "Resultados/AGORA_VAI/{}/{}/{} {} {}.txt".format(w, x, y, x, z)

f, axarr = plt.subplots(len(redes), len(modelos_resposta), figsize=(40,20))
f.suptitle("Intervalos de Confiância", fontsize=50)

for i in range(len(modelos_resposta)):
	res = modelos_resposta[i]
	est = res if res != "Tau-Exposure-Binario" else "Tau-Exposure"

	for j in range(len(redes)):
		rede = redes[j]
		MSE = []
		coi = []
	
		for k in range(len(betas)):
			beta = betas[k]
			ATE = genfromtxt(path(res, rede, est, beta), delimiter=',', skip_header=1)
    
			REAL = ATE[:, 0]
			ESTI = ATE[:, 1]
			erro = ((ESTI-REAL)**2)
			media = erro.mean()

			n = len(REAL)
			s = erro.std(ddof=1)
			t = stats.t.ppf(1-(alpha/2), n-1)
			inter = t*s/sqrt(n)

			MSE.append(media)
			coi.append((media-inter, media+inter))

		y_r = [MSE[x] - coi[x][1] for x in range(len(MSE))]
		Bars = axarr[j, i].bar(range(len(MSE)), MSE, yerr=y_r, alpha=0.2, align='center')
		x = np.array([plt.getp(item, 'x') + (plt.getp(item, 'width')/2) for item in Bars])
		y = ys[i][j]
		axarr[j, i].scatter(x, y, color='r')

		if(j == 0):
			axarr[j, i].set_title(res, fontsize=25)
		if(i == 0):
			axarr[j, i].set_ylabel(rede, fontsize=25)

		plt.sca(axarr[j, i])
		plt.xticks(range(len(MSE)), [str(beta) for beta in betas], fontsize=15)
		plt.yticks(fontsize=15)

plt.savefig("Imagens/Confidence Todos.png".format(rede))
