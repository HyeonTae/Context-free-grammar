lines = open('data_test.txt').read().strip().split('\n')
line = [l for l in lines]

for l in line:
    for pair in [[s for s in l.split('\t')]]:
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
        distance = max(depth)
        fname = "dev_distance/data_test_distance_" + str(distance) + ".txt"
        with open(fname, 'a') as f:
            f.write("%s\n" % l)
