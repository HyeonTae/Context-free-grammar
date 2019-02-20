import random
import numpy as np
import sys
N = 100
rb = 1
rc = 1

def s(l):
    return min(1, -3 * l / N + 3 if l <= 100 else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    global rc
    pc = rc * s(l)
    return np.random.choice(2, 1, p=[pc, 1 - pc])

def Ps():
    return np.random.choice(3, 1, p=[0.33, 0.33, 1-0.66])

def SS(words):
    l = len(words.replace("S", "")) + 2

    if(Pb(l) == 0):
        if(Pc(l) == 0):
            return S1(words)
        else:
            return S2(words)
    else:
        return S2(words)

def S1(words):
    if(Ps() == 0):
        words = words.replace("S", "aSa", 1)
    if(Ps() == 1):
        words = words.replace("S", "bSb", 1)
    else:
        words = words.replace("S", "cSc", 1)

    return SS(words)

def S2(words):
    if(Ps() == 0):
        words = words.replace("S", "aa", 1)
    if(Ps() == 1):
        words = words.replace("S", "bb", 1)
    else:
        words = words.replace("S", "cc", 1)

    return words

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
    f = open("grammar_reverse_data_N100.txt", 'w')
    words_list = []
    while(True):
        rb = random.uniform(0.7, 0.8)
        rc = random.uniform(0.7, 0.8)
        printProgress(len(words_list), 100000, 'Progress', 'Complete')
        if(len(words_list) >= 100000):
            break
        words = "S"
        sequence = []
        num = 0

        result = SS(words)

        if result not in words_list:
            words_list.append(result)
            size = int(len(result)/2)

            for i in range(1, size + 1):
                sequence.append(str(i))
            for i in range(size - 1, -1, -1):
                sequence.append(str(i))
            f.write("%s\t%s\n" % (" ".join(result), " ".join(sequence)))
            #print(result)
            #print(sequence)
        else:
            continue
 
if __name__ == "__main__":
    main()
