import numpy as np
import matplotlib.pyplot as plt

lines = open('grammar_data.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
distance = []
frequency = {}
for pair in pairs:
    distance.append(len(pair[0]))

for i in distance:
    count = frequency.get(i, 0)
    frequency[i] = count + 1

frequency_list = frequency.keys()

y = []
for i in frequency_list:
    print(i, frequency[i])
    y.append(frequency[i])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.set_xlim([0, 100])
ax.set_ylim([0, 500000])

ax.set_xlabel("distance")
ax.set_ylabel("frequency")

plt.plot(frequency_list, y)

plt.savefig('destance.png')
