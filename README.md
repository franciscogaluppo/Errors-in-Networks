# Estimation Errors in Network A/B Testing
This repository contains the code used to research about the estimation errors in network A/B testing due to sample variance and model misspecification, and how clusterization affects it. A simple new clusterization model is also proposed.

All of the researchers are from the Computer Science Department in Universidade Federal de Minas Gerais (UFMG), Brazil: 

1. Francisco Galuppo Azevedo - franciscogaluppo@dcc.ufmg.br
2. Bruno Demattos Nogueira - bruno.demattos@dcc.ufmg.br
3. Fabricio Murai - murai@dcc.ufmg.br
4. Ana Paula Couto Silva - ana.coutosilva@dcc.ufmg.br

To learn more about our research, read our papers:

## Estimation Errors in Network A/B Testing Due to Sample Variance and Model Misspecification

### Abstract:
Companies that offer services on the Web often rely on randomized experiments known as A/B tests for assessing the impact of development and business decisions. During an experiment, each user is randomly redirected to one of two versions of the website, called treatments. Several response models were proposed to describe the behavior of a user in a social network website as a function of the treatment assigned to her and to her neighbors. However, there is no consensus as to which model should be applied to a given dataset. In this work, we propose a new response model, derive theoretical limits for the estimation error of several models, and obtain empirical results for cases where the response model was misspecified.

|![](Imagens/Artigo2/final.png?raw=true)|
|:--:|
| *Mean Squared Error of the estimates of the Probit Model for 3 different networks* |

### Read the full paper:
1. [English](https://ieeexplore.ieee.org/abstract/document/8609643)
2. [Portuguese](https://arxiv.org/pdf/1803.03497)



## Análise de Algoritmos de Clusterizção para Experimentos Randomizados em Redes Sociais de Larga Escala

### Abstract:
Large companies conduct A/B tests to estimate the effect of changes in their websites. In these tests, users are randomly redirected to one of two versions of the site. However, in social networks, users that access different versions can influence each other if they are linked, making estimation more difficult. To minimize this interference, graph partitioning algorithms were proposed to find clusters of well-connected users (e.g. &epsilon;-net and FENNEL). All users within a cluster are redirected to the same version. In this work, we propose a parallel variant of &epsilon;-net and a new algorithm dubbed NoMAS, inspired on FENNEL. We present a theoretical analysis of the proposed algorithms’ scalability complemented by empirical results on the estimation accuracy.

|![](Imagens/Artigo2/Bruno.png?raw=true)|
|:--:|
| *Example for the parallel &epsilon;-net algorithm* |

### Read the full paper:
1. [Portuguese](https://sol.sbc.org.br/index.php/wperformance/article/view/3329)
