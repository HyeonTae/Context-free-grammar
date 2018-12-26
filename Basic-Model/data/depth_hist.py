import numpy as np
import matplotlib.pyplot as plt

lines = open('grammar_data.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
depths = []
frequency = {}
for pair in pairs:
    depth = []
    for i in pair[1].split(','):
        depth.append(int(i))
    depths.append(max(depth))

for i in depths:
    count = frequency.get(i, 0)
    frequency[i] = count + 1

frequency_list = frequency.keys()


'''
y = []
for i in frequency_list:
    print(i, frequency[i])
    y.append(frequency[i])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.set_xlim([0, 50])
ax.set_ylim([0, 500000])

ax.set_xlabel("depth")
ax.set_ylabel("frequency")

plt.plot(frequency_list, y)
'''

plt.hist(depths, bins=8)

plt.savefig('depth.png')
