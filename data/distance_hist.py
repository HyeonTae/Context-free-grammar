import numpy as np
import matplotlib.pyplot as plt

lines = open('data.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
distance = []
for pair in pairs:
    reverse_pair = list(reversed((pair[1].split(' '))))
    reverse_pair.append('0')
    depth = []
    count = -2
    compare = reverse_pair[0]
    for i in reverse_pair:
        if(i == compare):
            count = count + 1
            depth.append(count)
            count = -2
        else:
            count = count + 1
    depth.append(count)
    distance.append(max(depth))

plt.hist(distance, bins=10)
plt.savefig('distance.png')
