lines = open('data_test.txt').read().strip().split('\n')
line = [l for l in lines]

l2, l6, l10, l14, l18, l22, l26, l30, l34, l38, l42, l46, l50 = [],[],[],[],[],[],[],[],[],[],[],[],[]
l54, l58, l62, l66, l70, l74, l78, l82, l86, l90, l94, l98 = [],[],[],[],[],[],[],[],[],[],[],[]

for l in line:
    for pair in [[s for s in l.split('\t')]]:
        length = len(pair[0].split(' '))
        if length  == 2:
            l2.append(l)
        elif length == 6:
            l6.append(l)
        elif length == 10:
            l10.append(l)
        elif length == 14:
            l14.append(l)
        elif length == 18:
            l18.append(l)
        elif length == 22:
            l22.append(l)
        elif length == 26:
            l26.append(l)
        elif length == 30:
            l30.append(l)
        elif length == 34:
            l34.append(l)
        elif length == 38:
            l38.append(l)
        elif length == 42:
            l42.append(l)
        elif length == 46:
            l46.append(l)
        elif length == 50:
            l50.append(l)
        elif length == 54:
            l54.append(l)
        elif length == 58:
            l58.append(l)
        elif length == 62:
            l62.append(l)
        elif length == 66:
            l66.append(l)
        elif length == 70:
            l70.append(l)
        elif length == 74:
            l74.append(l)
        elif length == 78:
            l78.append(l)
        elif length == 82:
            l82.append(l)
        elif length == 86:
            l86.append(l)
        elif length == 90:
            l90.append(l)
        elif length == 94:
            l94.append(l)
        elif length == 98:
            l98.append(l)
        else:
            print("error")

with open("dev/data_test_line_2.txt", 'w') as f:
    for i in l2:
        f.write("%s\n" % i)
with open("dev/data_test_line_6.txt", 'w') as f:
    for i in l6:
        f.write("%s\n" % i)
with open("dev/data_test_line_10.txt", 'w') as f:
    for i in l10:
        f.write("%s\n" % i)
with open("dev/data_test_line_14.txt", 'w') as f:
    for i in l14:
        f.write("%s\n" % i)
with open("dev/data_test_line_18.txt", 'w') as f:
    for i in l18:
        f.write("%s\n" % i)
with open("dev/data_test_line_22.txt", 'w') as f:
    for i in l22:
        f.write("%s\n" % i)
with open("dev/data_test_line_26.txt", 'w') as f:
    for i in l26:
        f.write("%s\n" % i)
with open("dev/data_test_line_30.txt", 'w') as f:
    for i in l30:
        f.write("%s\n" % i)
with open("dev/data_test_line_34.txt", 'w') as f:
    for i in l34:
        f.write("%s\n" % i)
with open("dev/data_test_line_38.txt", 'w') as f:
    for i in l38:
        f.write("%s\n" % i)
with open("dev/data_test_line_42.txt", 'w') as f:
    for i in l42:
        f.write("%s\n" % i)
with open("dev/data_test_line_46.txt", 'w') as f:
    for i in l46:
        f.write("%s\n" % i)
with open("dev/data_test_line_50.txt", 'w') as f:
    for i in l50:
        f.write("%s\n" % i)
with open("dev/data_test_line_54.txt", 'w') as f:
    for i in l54:
        f.write("%s\n" % i)
with open("dev/data_test_line_58.txt", 'w') as f:
    for i in l58:
        f.write("%s\n" % i)
with open("dev/data_test_line_62.txt", 'w') as f:
    for i in l62:
        f.write("%s\n" % i)
with open("dev/data_test_line_66.txt", 'w') as f:
    for i in l66:
        f.write("%s\n" % i)
with open("dev/data_test_line_70.txt", 'w') as f:
    for i in l70:
        f.write("%s\n" % i)
with open("dev/data_test_line_74.txt", 'w') as f:
    for i in l74:
        f.write("%s\n" % i)
with open("dev/data_test_line_78.txt", 'w') as f:
    for i in l78:
        f.write("%s\n" % i)
with open("dev/data_test_line_82.txt", 'w') as f:
    for i in l82:
        f.write("%s\n" % i)
with open("dev/data_test_line_86.txt", 'w') as f:
    for i in l86:
        f.write("%s\n" % i)
with open("dev/data_test_line_90.txt", 'w') as f:
    for i in l90:
        f.write("%s\n" % i)
with open("dev/data_test_line_94.txt", 'w') as f:
    for i in l94:
        f.write("%s\n" % i)
with open("dev/data_test_line_98.txt", 'w') as f:
    for i in l98:
        f.write("%s\n" % i)
