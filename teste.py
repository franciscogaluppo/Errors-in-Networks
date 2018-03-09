import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def mult_hist(grafos, nomes_grafos, nome_estimador, nome_gerador, beta, bins, path, cor='r'):
	#hard 3
	matplotlib.rcParams.update({'font.size': 22})
	f, axes = plt.subplots(1, 3, sharey=True, figsize=(25, 10))
	f.text(0.5, 0.04, 'ATE Estimado', ha='center', fontsize=25)
	f.text(0.04, 0.5, 'Frequência Relativa', va='center', rotation='vertical', fontsize=25)
	# plt.ylabel("Frequência Relativa")

	j = 0
	for ax in axes:
		ATE_est = grafos[j][1].mean()
		ATE_real = grafos[j][0].mean()
		erro = ((grafos[j][1] - grafos[j][0])**2).mean()
		var_real = grafos[j][0].var()
		var_est = grafos[j][1].var()

		# print("{} - {}{} - {}\nATE_est: {}\nATE_real: {}\nMSE: {}\nvar real: {}\nvar est: {}\n".format(
		# 	nomes_grafos[j], nome_gerador, beta, nome_estimador, ATE_est, ATE_real, erro, var_real, var_est
		# ))

		print("{} - {}{} - {}\nMSE: {}\n".format(nomes_grafos[j], nome_gerador, beta, nome_estimador, erro))

		ax.set_title(nomes_grafos[j], fontsize=25)
		# ax.set(adjustable='box-forced', aspect='equal')


		# ax.set_title("{} - {}({}, {}, {}) - {}".format(
		# 	nomes_grafos[j], nome_gerador, beta[0], beta[1], beta[2], nome_estimador
		# ))

		n, b, patches = ax.hist(grafos[j][1], bins=bins, histtype='bar',
			weights=np.zeros_like(grafos[j][1]) + 1. / grafos[j][1].size)
		ax.axvline(ATE_real, color='black', linestyle='dashed', linewidth=2)

		# cores
		for patch in patches:
			patch.set_facecolor(cor)

		# # Legenda
		# vals = "Média do ATE estimado: {:.3}\nMédia do ATE real: {:.3}\nMSE Empírico: {:.3}\nVariância: {:.3}\n".format(ATE_est, ATE_real, erro, var)
		# handles, labels = ax.get_legend_handles_labels()
		# handles.append(mpatches.Patch(color='none', label=vals))
		# plt.legend(handles=handles, fontsize=8, frameon=False)

		j += 1

	# Gera o gráfico
	plt.suptitle("{}({}, {}, {}) - {}".format(nome_gerador, beta[0], beta[1], beta[2], nome_estimador), fontsize=35)
	plt.savefig("{}{}({}, {}, {}) - {}". format(path, nome_gerador, beta[0],
		beta[1], beta[2], nome_estimador) + ".png")