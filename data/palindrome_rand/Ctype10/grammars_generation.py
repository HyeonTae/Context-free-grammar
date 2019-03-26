import random
import numpy as np
import sys
N = 100
rb = 1
rc = 1

def s(l):
    global N
    return min(1, -3 * l / N + 3 if l <= N else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    global rc
    if(l >= 5):
        rc = 0
    return np.random.choice(2, 1, p=[rc, 1 - rc])

def Ps():
    return np.random.choice(10, 1, p=[0.1, 0.1, 0.1, 0.1, 0.1,
                                     0.1, 0.1, 0.1, 0.1, 0.1])

def S(words, label):
    l = len(words.replace("S", "").replace("*", ""))

    if(Pb(l) == 0):
        return S1(words, label)
    else:
        return S2(words, label)

def S1(words, label):
    if(Ps() == 0):
        words = words.replace("*S", "aSa", 1)
    elif(Ps() == 1):
        words = words.replace("*S", "bSb", 1)
    elif(Ps() == 2):
        words = words.replace("*S", "cSc", 1)
    elif(Ps() == 3):
        words = words.replace("*S", "dSd", 1)
    elif(Ps() == 4):
        words = words.replace("*S", "eSe", 1)
    elif(Ps() == 5):
        words = words.replace("*S", "fSf", 1)
    elif(Ps() == 6):
        words = words.replace("*S", "gSg", 1)
    elif(Ps() == 7):
        words = words.replace("*S", "hSh", 1)
    elif(Ps() == 8):
        words = words.replace("*S", "iSi", 1)
    else:
        words = words.replace("*S", "jSj", 1)

    label = label.replace("*S", "1S0", 1)
    return SS(words, label)

def S2(words, label):
    if(Ps() == 0):
        words = words.replace("*S", "aa", 1)
    elif(Ps() == 1):
        words = words.replace("*S", "bb", 1)
    elif(Ps() == 2):
        words = words.replace("*S", "cc", 1)
    elif(Ps() == 3):
        words = words.replace("*S", "dd", 1)
    elif(Ps() == 4):
        words = words.replace("*S", "ee", 1)
    elif(Ps() == 5):
        words = words.replace("*S", "ff", 1)
    elif(Ps() == 6):
        words = words.replace("*S", "gg", 1)
    elif(Ps() == 7):
        words = words.replace("*S", "hh", 1)
    elif(Ps() == 8):
        words = words.replace("*S", "ii", 1)
    else:
        words = words.replace("*S", "jj", 1)

    label = label.replace("*S", "10", 1)
    return words, label

def SS(words, label):
    l = len(words.replace("*", ""))

    if(Pc(l) == 0):
        return SS(words + "S", label + "S")
    else:
        return words, label

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 50):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
    if(iteration == total):
        sys.stdout.write('\n')
    sys.stdout.flush()

def main():
    global rb
    global rc
    global N
    f = open("grammar_data.txt", 'w')
    words_list = []
    while(True):
        rb = random.uniform(0.9, 0.95)
        rc = random.uniform(0.4, 0.6)
        printProgress(len(words_list), 10000, 'Progress', 'Complete')
        if(len(words_list) >= 10000):
            break
        words = "*S"
        label = "*S"
        labels = []
        num = 0

        result, label= SS(words, label)

        while(True):
            if "*" not in result:
                break
            elif "*S" in result:
                point = result.find('*S')
                result, label = S(result, label)
                if(result.find('S', point + 2) != -1):
                    result = result.replace(result[result.find('S', point + 2)], "*S", 1)
                    label = label.replace(label[label.find('S', point + 2)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)
                    label = label.replace("S", "*S", 1)

        if result not in words_list:
            words_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            label = label[:len(label) if len(label) <= N else N]
            for i in label:
                if(i == "1"):
                    num = num + 1
                    labels.append(str(num))
                else:
                    num = num - 1
                    labels.append(str(num))
            f.write("%s\t%s\n" % (" ".join(result), " ".join(labels)))

        else:
            continue
 
if __name__ == "__main__":
    main()
