lines = open('grammar_data.txt').read().strip().split('\n')
line = [l for l in lines]

for l in line:
    for pair in [[s for s in l.split('\t')]]:
        length = len(pair[1].split(' '))
        fname = "dev_length/data_test_length_" + str(length) + ".txt"
        with open(fname, 'a') as f:
            f.write("%s\n" % l)
