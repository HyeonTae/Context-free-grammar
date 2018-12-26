import numpy as np
import matplotlib.pyplot as plt

lines = open('grammar_data.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
depths = []
for pair in pairs:
    depth = []
    for i in pair[1].split(','):
        depth.append(int(i))
    depths.append(max(depth))

plt.hist(depths, bins=10)
plt.savefig('depth.png')
