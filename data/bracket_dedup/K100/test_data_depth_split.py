lines = open('data_test.txt').read().strip().split('\n')
line = [l for l in lines]

for l in line:
    for pair in [[s for s in l.split('\t')]]:
        depths = []
        for i in pair[1].split(' '):
            depths.append(int(i))
        depth = max(depths)
        fname = "dev_depth/data_test_depth_" + str(depth) + ".txt"
        with open(fname, 'a') as f:
            f.write("%s\n" % l)
