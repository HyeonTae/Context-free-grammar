import random
import numpy as np
import sys
N = 100
rb = 1
rc = 1

def s(l):
    return min(1, - 3 * l / N + 3 if l <= N else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Ps1():
    return np.random.choice(2, 1, p=[0.5, 0.5])

def Ps2():
    return np.random.choice(4, 1, p=[0.25, 0.25, 0.25, 0.25])

def S(words, label):
    l = len(words.replace("S", ""))

    if(Pb(l) == 0):
        return S1(words, label)
    else:
        return S2(words, label)

def S1(words, label):
    ps1=Ps1()
    if(Ps1() == 0):
        words = words.replace("S", "aSa", 1)
    elif(ps1 == 1):
        words = words.replace("S", "bSb", 1)

    label = label.replace("S", "1S0", 1)
    return S(words, label)

def S2(words, label):
    ps2=Ps2()
    if(ps2 == 0):
        words = words.replace("S", "aa", 1)
        label = label.replace("S", "10", 1)
    elif(ps2 == 1):
        words = words.replace("S", "bb", 1)
        label = label.replace("S", "10", 1)
    elif(ps2 == 2):
        words = words.replace("S", "a", 1)
        label = label.replace("S", "2", 1)
    elif(ps2 == 3):
        words = words.replace("S", "b", 1)
        label = label.replace("S", "2", 1)

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
    brackets_list = []
    while(True):
        rb = random.uniform(0.9, 0.95)
        printProgress(len(brackets_list), 100000, 'Progress', 'Complete')
        if(len(brackets_list) >= 100000):
            break
        result = "S"
        label = "S"
        labels = []
        num = 0

        result, label= S(result, label)

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            label = label[:len(label) if len(label) <= N else N]
            for i in label:
                if(i == "1"):
                    num = num + 1
                    labels.append(str(num))
                elif(i == "0"):
                    num = num - 1
                    labels.append(str(num))
                else:
                    labels.append(str(num))
                 
            f.write("%s\t%s\n" % (" ".join(result), " ".join(labels)))

        else:
            continue
 
if __name__ == "__main__":
    main()
