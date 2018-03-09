# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def setBoxColors(bp):
    setp(bp['boxes'][0], color='blue')
    setp(bp['caps'][0], color='blue')
    setp(bp['caps'][1], color='blue')
    setp(bp['whiskers'][0], color='blue')
    setp(bp['whiskers'][1], color='blue')
    setp(bp['fliers'][0], color='blue')
    setp(bp['fliers'][1], color='blue')
    setp(bp['medians'][0], color='blue')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    setp(bp['fliers'][2], color='red')
    setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

RUNS = 1000
labels = [1,2,5,10,20,50,100]
indices = [i-1 for i in labels]
positions = [0,1,2, 4,5,6, 8,9,10, 12,13,14, 16,17,18, 20,21,22, 24,25,26]
print(positions)
nseeds=[2,4,8]

data = np.zeros((RUNS,len(indices)*len(nseeds)))
for kx,n in enumerate(nseeds):
    with open('saida{}'.format(n),'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter=' ')
        for ix, line in enumerate(tsvin):
            for jx, ind in enumerate(indices):
                data[ix,jx*len(nseeds)+kx] = line[ind]

matplotlib.rc('font', family='Arial')
plt.boxplot(data, positions=positions, whis='range')
plt.title('Wiki-Vote')

plt.xlabel('iteration')
plt.xlabel(u'iteração')

plt.xticks(np.arange(1,26,4),labels)
plt.ylabel('number of messages')
plt.ylabel(u'número de mensagens')

plt.yscale('log')
plt.grid(True)
plt.ylim(ymin=1)
plt.savefig('communication_Wiki-Vote.pdf')

