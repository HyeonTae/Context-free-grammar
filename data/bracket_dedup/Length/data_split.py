length = list(range(60, 201, 20))

for k in length:
    fileName = "grammar_data_N" + str(k) + ".txt"
    lines = open(fileName).read().strip().split('\n')
    line = [l for l in lines]
    even = []
    odd = []
    for l in line:
        for pair in [[s for s in l.split('\t')]]:
            length = len(pair[1].split(' '))/2
            if length % 2 == 0:
                even.append(l)
            else:
                odd.append(l)

    with open("N" + str(k) + "_data_train.txt", 'w') as f:
        for i in even:
            f.write("%s\n" % i)
    with open("N" + str(k) + "_data_test.txt", 'w') as f:
        for i in odd:
            f.write("%s\n" % i)
