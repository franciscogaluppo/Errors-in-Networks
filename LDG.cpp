#include <bits/stdc++.h>
using namespace std;

int main(int argc, char const *argv[])
{
	//tamanho do vetor
	int n = atoi(argv[1]);
	vector <vector<int>> m (n);

	//Cria a lista de adjacencia
	FILE *f = fopen("Datasets/SlashDot/set.txt", "r");
	if (f == NULL){
		printf("Arquivo set nao encontrado\n");
		return 1;
	}
	int a, b;
	while (fscanf(f, 	"%i %i", &a, &b) != EOF){
		m[a].push_back(b);
		m[b].push_back(a);
	}
	fclose(f);

	int clusters = atoi(argv[2]);

	//vetor que vai guardar a que comunidade pertence cada vertice
	int centro[n];
	int tamanho[clusters];
	for(int i = 0; i < n; i++){
		centro[i] = -1;
		if (i < clusters)
			tamanho[i] = 0;
	}

	clock_t t = clock();

	queue <int> fila;
	for(int i = 0; i < clusters; i++){
		fila.push(i);
		centro[i] = i;
		tamanho[i] += 1;
	}

	double limite = (double) n / clusters;

	//bfs
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
				coeficiente[j] *= (1 - (double) tamanho[j]/limite);
			

			//descobre a comunidade que tem o maior coeficiente
			int maior = 0;
			for(int j = 1; j < clusters; j++){
				if (coeficiente[j] > coeficiente[maior])
					maior = j;
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


	//Proximas iteracoes
	int iteracoes = atoi(argv[3]) - 1;
	for(int k = 0; k < iteracoes; k++){
		vector <int> vis (n, 0);
		fila.push(0);

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
					coeficiente[j] *= (1 - (double) tamanho[j]/limite);

				//descobre a comunidade que tem o maior coeficiente
				int maior = 0;
				for(int j = 1; j < clusters; j++){
					if (coeficiente[j] > coeficiente[maior])
						maior = j;
					else if (coeficiente[j] == coeficiente[maior])
							maior = tamanho[maior] > tamanho[j]? j : maior;
				}

				tamanho[centro[m[u][i]]] -= 1;
				//coloca ele na maior comunidade
				centro[m[u][i]] = maior;
				tamanho[maior] += 1;

				//adiciona na fila
				fila.push(m[u][i]);
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


	FILE* escrita = fopen("Datasets/SlashDot/comunidades.txt", "w");
	for(int i = 0; i < clusters; i++){
		for (int j = 0; j < n; j++)
			if (centro[j] == i)
				fprintf(escrita, "%i ", j);
		fprintf(escrita, "\n");
	}
	fclose(escrita);

	return 0;
}
