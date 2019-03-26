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

with open("data_train.txt", 'w') as f:
    for i in even:
        f.write("%s\n" % i)
with open("data_test.txt", 'w') as f:
    for i in odd:
        f.write("%s\n" % i)
