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
		//se comentar a linha de baixo o grafo passa a ser dirigido
		m[b].push_back(a);
	}
	fclose(f);

	//numero de clusters
	int clusters = atoi(argv[2]);

	//vetor que vai guardar a que comunidade pertence cada vertice
	vector <int> centro (n, -1);
	//vetor que guarda o tamanho de cada cluster
	vector <int> tamanho (clusters, 0);

	//define as comunidades dos primeiros vertices
	for(int i = 0; i < clusters; i++){
		centro[rand() % n] = i;
		tamanho[i] += 1;
	}

	//capacidade maxima de cada cluster
	double limite = (double) n / clusters;
	//o tanto que pode variar o tamanho
	//limite *= 1.1;


	int iteracoes = atoi(argv[3]);
	double alpha = atof(argv[4]);
	for(int k = 0; k < iteracoes; k++){

		//quais vertices ja foram visitados nessa iteracao
		vector <int> vis (n, 0);

		queue <int> fila;
		fila.push(rand() % n);

		for (int l = 0; l < n; l++){
			//se ja foi visitado continua
			if (vis[l])
				continue;

			queue <int> fila;
			fila.push(l);

			//bfs
			while(fila.size()){
				int u = fila.front();
				fila.pop();

				if(vis[u])
					continue;

				//marca como visitado
				vis[u] = 1;
				//adiciona os vizinhos na fila
				for(int i = 0; i < m[u].size(); i++)
					if(!vis[m[u][i]])
						fila.push(m[u][i]);

				//se, na primeira iteracao, ja tiver comunidade, pula
				if(!k && centro[u] > -1)
					continue;

				vector <double> coeficiente (clusters, 0);

				for(int i = 0; i < m[u].size(); i++){
					int indice = centro[m[u][i]];
					if (indice > -1)
						coeficiente[indice] += 1;
				}

				for(int i = 0; i < clusters; i++)
					coeficiente[i] -= alpha*tamanho[i];

				//descobre qual e o cluster com maior coeficiente
				int maior = 0;
				for(int j = 1; j < clusters; j++){
					if (coeficiente[j] > coeficiente[maior])
						maior = j;
					//o criterio de desempate e o tamanho
					else if (coeficiente[j] == coeficiente[maior])
						maior = tamanho[maior] > tamanho[j]? j : maior;
					}

				centro[u] = maior;
				tamanho[maior] += 1;
			}
		}

		if (k < iteracoes - 1)
			for(int i = 0; i < clusters; i++)
				tamanho[i] = 0;
	}

	for(int i = 0; i < clusters; i++)
		printf("O tamanho do cluster %i e %i\n", i + 1, tamanho[i]);

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
