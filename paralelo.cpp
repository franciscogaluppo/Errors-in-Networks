#include <bits/stdc++.h>
using namespace std;

int max(int a, int b){
	if (a > b) return a;
	return b;
}

int main(int argc, char const *argv[])
{
	srand(atoi(argv[7]));

	char grafo[200];
	strcpy(grafo, "Datasets/");
	strcat(grafo, argv[1]);	
	strcat(grafo, "/set.txt");

	//tamanho o vetor
	int n = atoi(argv[2]);
	vector <vector<int>> m (n);

	//mapa para o caso em que os vertice nao estao numerados de 0 ate n - 1
	map <int, int> mapa;
	int index = 0;

	//Cria a lista de adjacencia
	FILE *f = fopen(grafo, "r");
	if (f == NULL){
		printf("Arquivo set nao encontrado\n");
		return 1;
	}
	int a, b;
	while (fscanf(f, "%i %i", &a, &b) != EOF){
		if(!mapa.count(a)){
			mapa[a] = index;
			index++;
		}
		if(!mapa.count(b)){
			mapa[b] = index;
			index++;
		}
		a = mapa[a]; 
		b = mapa[b];

		if (a == b)
			continue;

		m[a].push_back(b);
		//se comentar a linha de baixo o grafo passa a ser dirigido
		//m[b].push_back(a);
	}
	fclose(f);

	//numero de clusters
	int clusters = atoi(argv[3]);

	//vetor que vai guardar a que comunidade pertence cada vertice
	vector <int> centro (n, -1);
	//vetor que guarda o tamanho de cada cluster
	vector <int> tamanho (clusters, 0);


	int nMaq = atoi(argv[6]);
	vector <int> maq(n); //o vertice i esta na maquina maq[i]
	for(int i = 0; i < n; i++)
		maq[i] = rand() % nMaq;


	for(int i = 0; i < nMaq; i++){
		int aux = 0;
		for(int j = 0; j < n; j++)
			aux += (maq[j] == i);
		//printf("%i ", aux);

		set<int> s;
		for(int j = 0; j < n; j++)
			if(maq[j] == i){
				for(int k = 0; k < m[j].size(); k++)
					if(maq[m[j][k]] != i)
						s.insert(m[j][k]);
			}

		//printf("%i\n", (int) s.size());
	}

	vector <int> atual(n, -1);

	//define as comunidades dos primeiros vertices
	for(int i = 0; i < clusters; i++){
		int vertice = rand() % n;
		centro[vertice] = i;
		atual[vertice] = i;
		tamanho[i] += 1;
	}

	int iteracoes = atoi(argv[4]);
	double alpha = atof(argv[5]);

	int custo = 0;

	for(int k = 0; k < iteracoes; k++){

		//quais vertices ja foram visitados nessa iteracao
		vector <int> vis (n, 0);

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

				for(int i = 0; i < clusters; i++){
					coeficiente[i] = max(coeficiente[i], 1);
					coeficiente[i] /= pow(tamanho[i], alpha);
				}
				//descobre qual e o cluster com maior coeficiente
				int maior = 0;
				for(int j = 1; j < clusters; j++){
					if (coeficiente[j] > coeficiente[maior])
						maior = j;
					//o criterio de desempate e o tamanho
					else if (coeficiente[j] == coeficiente[maior])
						maior = tamanho[maior] > tamanho[j]? j : maior;
				}

				// centro[u] = maior;
				tamanho[maior] += 1;
				atual[u] = maior;
			}
		}

		//agora tem que ver o custo de mandar pra todo mundo
		for(int i = 0; i < n; i++){
			if(centro[i] == atual[i])
				continue;
			set<int> s;
			for(int j = 0; j < m[i].size(); j++)
				if(maq[i] != maq[m[i][j]])
					s.insert(maq[m[i][j]]);
			custo += s.size();
		}

		for(int i = 0; i < n; i++){
			custo += centro[i] != atual[i];
			centro[i] = atual[i];
		}

		if (k < iteracoes - 1)
			for(int i = 0; i < clusters; i++)
				tamanho[i] = 0;
	}

	int maior = tamanho[0];
	int menor = maior;
	for(int i = 0; i < clusters; i++){
		//printf("Tamanho do cluster %i = %i\n", i, tamanho[i]);
		if(tamanho[i] > maior)
			maior = tamanho[i];
		else if (tamanho[i] < menor)
			menor = tamanho[i];
	}

	//printf("Diferenca entre os clusters = %lf\n", (double) maior/menor);
	printf("%i\n", custo);

	char com[200];
	sprintf(com, "Datasets/%s/comunidades.txt", argv[1]);
	FILE* escrita = fopen(com, "w");
	for(int i = 0; i < clusters; i++){
		for (int j = 0; j < n; j++)
			if (centro[j] == i)
				fprintf(escrita, "%i ", j);
		fprintf(escrita, "\n");
	}
	fclose(escrita);

	return 0;
}
