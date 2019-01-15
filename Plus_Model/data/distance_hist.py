import numpy as np
import matplotlib.pyplot as plt

lines = open('grammar_data.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
distance = []
for pair in pairs:
    depth = []
    count = 0
    for i in pair[1].split(' '):
        if(int(i) == 0):
            count = count + 1
            depth.append(count)
            count = 0
        else:
            count = count + 1
    depth.append(count)
    distance.append(max(depth))

plt.hist(distance, bins=10)
plt.savefig('distance.png')
