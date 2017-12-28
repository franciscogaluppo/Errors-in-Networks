#include <bits/stdc++.h>
using namespace std;

int main(int argc, char const *argv[])
{
  //tamanho do vetor
  int n = atoi(argv[1]);
	vector <vector<int>> m (n);

  //Cria a lista de adjacencia
  FILE *grafo = fopen("Datasets/SlashDot/set.txt", "r");
	int a, b;
	while (fscanf(grafo, 	"%i %i", &a, &b) != EOF){
		m[a].push_back(b);
		m[b].push_back(a);
	}
  fclose(grafo);

  //cria um vetor para guardar as comunidades e inicializa tudo com o -1
  vector <int> comunidades (n, -1);

  FILE *comu = fopen("Datasets/SlashDot/comunidades.txt", "r");
  char line[200000];
  int count = 0;
  while(fscanf(comu, " %[^\n]", line) != EOF){
    int i = 0;
    while(i < strlen(line)){
      int num = 0;
      while(i < strlen(line) && line[i] >= '0' && line[i] <= '9'){
        num *= 10;
        num += line[i] -'0';
        i++;
      }

      comunidades[num] = count;
      i++;
    }

    count++;
  }

  double arestasInternas = 0, totalArestas = 0;
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m[i].size(); j++){
      totalArestas++;
      if(comunidades[i] == comunidades[m[i][j]])
        arestasInternas++;
    }

  printf("Coeficiente de arestas cortadas = %lf\n", 1.0 - arestasInternas/totalArestas);


  return 0;
}
