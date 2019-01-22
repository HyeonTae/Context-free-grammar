import numpy as np
import matplotlib.pyplot as plt

<<<<<<< HEAD
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
=======
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
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
        else:
            count = count + 1
    depth.append(count)
    distance.append(max(depth))

<<<<<<< HEAD
#print(distance)
=======
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
plt.hist(distance, bins=10)
plt.savefig('distance.png')
