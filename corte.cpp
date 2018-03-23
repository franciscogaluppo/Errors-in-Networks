#include <bits/stdc++.h>
using namespace std;

int main(int argc, char const *argv[])
{
  char grafo[200];
  strcpy(grafo, "Datasets/");
  strcat(grafo, argv[1]); 
  strcat(grafo, "/set.txt");

  //tamanho do vetor
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
    m[b].push_back(a);
  }
  fclose(f);

  //cria um vetor para guardar as comunidades e inicializa tudo com o -1
  vector <int> comunidades (n, -1);

  char com[200];
  sprintf(com, "Datasets/%s/comunidades.txt", argv[1]);
  FILE *comu = fopen(com, "r");
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

  printf("%lf\n", 1.0 - arestasInternas/totalArestas);


  return 0;
}
