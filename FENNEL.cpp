#include <bits/stdc++.h>
using namespace std;

int main(int argc, char const *argv[])
{
	int n = atoi(argv[1]);
	vector <vector<int>> m (n);

	FILE *f = fopen("grafo.txt", "r");
	int a, b;
	while (fscanf(f, 	"%i %i", &a, &b) != EOF){
		m[a].push_back(b);
		m[b].push_back(a);
	}

	int clusters = atoi(argv[2]);

	//Vetor que vai guardar a que comunidade pertence cada vertice
	int centro[n];
	int tamanho[clusters];

	double alpha = stod(argv[3]);

	clock_t t = clock();

	//coloca os 'clusters' primeiros vertices como centro de suas comunidades e o tamanho de cada grupo como 1
	for(int i = 0; i < clusters*clusters; i++){
		tamanho[i % clusters] = clusters;
		centro[i] = i % clusters;
	}


	for(int i = clusters*clusters; i < n; i++){
		double coeficiente[clusters];
		for(int j = 0; j < clusters; j++)
			coeficiente[j] = 0;


		//itera pelos vizinhos e soma ao coeficiente de cada grupo o numero de vizinhos
		for (int j = 0; j < m[i].size(); j++){
			if (m[i][j] > i)
				continue;
			int indice = centro[m[i][j]];
			coeficiente[indice] += 1;
		}


		//calcula o coeficiente de cada cluster
		for(int j = 0; j < clusters; j++)
			coeficiente[j] -= alpha*tamanho[j];


		//descobre a comunidade que tem o maior coeficiente
		int maior = 0;
		for(int j = 1; j < clusters; j++)
			if (coeficiente[j] > coeficiente[maior])
				maior = j;

		// printf("comunidade escolhida: %i\n", maior);

		//O vertice i sera colocado na comunidade maior
		centro[i] = maior;
		tamanho[maior] += 1;

		// if(i % 1000 == 0)
		// 	printf("%i\n", i);


	}

	t = clock() - t;
	double tempo = (double) t / CLOCKS_PER_SEC;

	for(int i = 0; i < clusters; i++)
		printf("O tamanho do cluster %i e %i\n", i + 1, tamanho[i]);

	printf("Tempo decorrido: %lf\n", tempo);

	FILE* escrita = fopen("comunidades.txt", "w");
	for(int i = 0; i < clusters; i++){
		for (int j = 0; j < n; j++)
			if (centro[j] == i)
				fprintf(escrita, "%i ", j);
		fprintf(escrita, "\n");
	}


	return 0;
}
