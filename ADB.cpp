#include <bits/stdc++.h>
using namespace std;

double pot(double a, double b){
	for(int i = 1; i < b; i++)
		a *= a;
	return a;
}

int main(int argc, char const *argv[])
{
	//tamanho do vetor
	int n = atoi(argv[1]);
	vector <vector<int>> m (n);

	//Cria a lista de adjacencia
	FILE *f = fopen("set.txt", "r");
	if (f == NULL){
		printf("Arquivo set nao encontrado\n");
		return 1;
	}
	int a, b;
	while (fscanf(f, 	"%i %i", &a, &b) != EOF){
		m[a].push_back(b);
		//se descomentar a linha de baixo o grafo deixa de ser dirigido
		//m[b].push_back(a);
	}
	fclose(f);

	//numero de clusters
	int clusters = atoi(argv[2]);

	//vetor que vai guardar a que comunidade pertence cada vertice
	int centro[n];
	//vetor que guarda o tamanho de cada cluster
	int tamanho[clusters];
	for(int i = 0; i < n; i++){
		centro[i] = -1;
		if (i < clusters)
			tamanho[i] = 0;
	}

	clock_t t = clock();

	//fila usada para fazer a bfs
	queue <int> fila;
	for(int i = 0; i < clusters; i++){
		fila.push(i);
		centro[i] = i;
		tamanho[i] += 1;
	}

	//capacidade maxima de cada cluster
	double expoente = atof(argv[4]);

	for(int k = 0; k < n; k++){
		if(centro[k] > -1)
			continue;
			//bfs

		fila.push(k);
		while(fila.size()){
			int u = fila.front();
			fila.pop();

			for(int i = 0; i < m[u].size(); i++){
				//se ja foi visitado vai pro proximo
				if(centro[m[u][i]] > -1)
					continue;

				//se nao foi visitado, escolhe uma comunidade e coloca na fila
				vector <double> coeficiente (clusters, 0);

				//calcula o numero de vizinhos com cada comunidade
				for (int j = 0; j < m[u].size(); j++){
					int indice = centro[m[u][j]];
					if (indice > -1)
						coeficiente[indice] += 1;
				}

				//calcula o coeficeinte
				for(int j = 0; j < clusters; j++)
					coeficiente[j] /= pot(tamanho[j], expoente);

				//descobre a comunidade que tem o maior coeficiente
				int maior = 0;
				for(int j = 1; j < clusters; j++){
					if (coeficiente[j] > coeficiente[maior])
						maior = j;
					//criterio de desempate e o tamanho da comunidade
					else if (coeficiente[j] == coeficiente[maior])
							maior = tamanho[maior] > tamanho[j]? j : maior;
				}

				//coloca ele na maior comunidade
				centro[m[u][i]] = maior;
				tamanho[maior] += 1;

				//adiciona na fila
				fila.push(m[u][i]);
			}
		}
	}


	//Proximas iteracoes
	int iteracoes = atoi(argv[3]) - 1;
	for(int k = 0; k < iteracoes; k++){
		vector <int> vis (n, 0);
		for (int l = 0; l < n; l++){
			if (vis[l])
				continue;

			fila.push(l);

			//bfs
			while(fila.size()){
				int u = fila.front();
				fila.pop();

				for(int i = 0; i < m[u].size(); i++){
					//se ja foi visitado vai pro proximo
					if(vis[m[u][i]])
						continue;

					vis[m[u][i]] = 1;
					//se nao foi visitado, escolhe uma comunidade e coloca na fila
					vector <double> coeficiente (clusters, 0);

					for (int j = 0; j < m[u].size(); j++){
						int indice = centro[m[u][j]];
						coeficiente[indice] += 1;
					}

					for(int j = 0; j < clusters; j++)
						coeficiente[j] /= pot(tamanho[j], expoente);

					//descobre a comunidade que tem o maior coeficiente
					int maior = 0;
					for(int j = 1; j < clusters; j++){
						if (coeficiente[j] > coeficiente[maior])
							maior = j;
						else if (coeficiente[j] == coeficiente[maior])
								maior = tamanho[maior] > tamanho[j]? j : maior;
					}

					//tira da comunidade atual
					tamanho[centro[m[u][i]]] -= 1;
					//coloca ele na maior comunidade
					centro[m[u][i]] = maior;
					tamanho[maior] += 1;

					//adiciona na fila
					fila.push(m[u][i]);
				}
			}
		}
	}

	t = clock() - t;
	double tempo = (double) t / CLOCKS_PER_SEC;
	printf("Tempo decorrido: %lf\n", tempo);

	for(int i = 0; i < clusters; i++)
		printf("O tamanho do cluster %i e %i\n", i + 1, tamanho[i]);

	// for(int i = 0; i < n; i++)
	// 	printf("%i\n", centro[i]);


	FILE* escrita = fopen("comunidades.txt", "w");
	for(int i = 0; i < clusters; i++){
		for (int j = 0; j < n; j++)
			if (centro[j] == i)
				fprintf(escrita, "%i ", j);
		fprintf(escrita, "\n");
	}
	fclose(escrita);

	return 0;
}
