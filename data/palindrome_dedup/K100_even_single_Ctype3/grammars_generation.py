import random
import numpy as np
import sys
import math

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
    return np.random.choice(3, 1, p=[0.333, 0.333, 1-0.666])

def S(words):
    l = len(words.replace("S", ""))

    if(Pb(l) == 0):
        return S1(words)
    else:
        return S2(words)

def S1(words):
    ps1=Ps1()
    if(Ps1() == 0):
        words = words.replace("S", "aSd", 1)
    elif(ps1 == 1):
        words = words.replace("S", "bSe", 1)
    elif(ps1 == 2):
        words = words.replace("S", "cSf", 1)

    return S(words)

def S2(words):
    ps1=Ps1()
    if(ps1 == 0):
        words = words.replace("S", "ad", 1)
    elif(ps1 == 1):
        words = words.replace("S", "be", 1)
    elif(ps1 == 2):
        words = words.replace("S", "cf", 1)

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

def answer_function(data):
    result = []
    num = 0
    m = int(len(data)/2)
    for i in range(m):
        num += 1
        result.append(str(num))
    #result.append(str(num))
    for i in range(m):
        num -= 1
        result.append(str(num))

    return " ".join(result)

def main():
    global rb
    global rc
    global N
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.9, 0.99)
        printProgress(len(brackets_list), 100000, 'Progress', 'Complete')
        if(len(brackets_list) >= 100000):
            break
        result = "S"
        num = 0

        result = S(result)

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            label = answer_function(result)
            result = result[:math.ceil(len(result)/2)]  + result[math.ceil(len(result)/2):]
                 
            f.write("%s\t%s\n" % (" ".join(result), label))

        else:
            continue
 
if __name__ == "__main__":
    main()
