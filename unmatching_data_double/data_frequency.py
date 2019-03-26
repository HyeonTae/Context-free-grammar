lines = open('grammar_unmatching_data_N100.txt').read().strip().split('\n')
pairs = [[s for s in l.split('\t')] for l in lines]
depths = []
unmatching = 0
matching = 0
depth_cp = []
for pair in pairs:
    depth = []
    for i in pair[1].split(' '):
        depth.append(int(i))
        depth_cp.append(int(i))
    depths.append(max(depth))

for i in depths:
    if i > 1 :
        unmatching += 1
    else:
        matching += 1

error = 0
for i in depth_cp:
    if i > 0:
        error += 1

print("matching data: %0.2f" % (matching/len(depths)*100),"%")
print("unmatching data: %0.2f" % (unmatching/len(depths)*100),"%")
print("unmatching rate: %0.2f" % (error/len(depth_cp)*100),"%")
