lines = open('grammar_data.txt').read().strip().split('\n')
line = [l for l in lines]
even = []
odd = []
for l in line:
    for pair in [[s for s in l.split('\t')]]:
        length = len(pair[1].split(' '))
        if length % 2 == 0:
            even.append(l)
        else:
            odd.append(l)

train = []
test = []
for l in even:
    for pair in [[s for s in l.split('\t')]]:
        length = len(pair[1].split(' '))/2
        if length % 2 == 0:
            train.append(l)
        else:
            test.append(l)

for l in odd:
    for pair in [[s for s in l.split('\t')]]:
        length = (len(pair[1].split(' ')) + 1)/2
        if length % 2 == 0:
            train.append(l)
        else:
            test.append(l)

with open("data_train.txt", 'w') as f:
    for i in train:
        f.write("%s\n" % i)
with open("data_test.txt", 'w') as f:
    for i in test:
        f.write("%s\n" % i)
