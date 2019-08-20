import random
import numpy as np
import sys
N = 100
rb = 1

def s(l):
    return min(1, - 2.5 * l / N + 3 if l <= N else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pe(n):
    p = [0.3]
    for i in range(n, 0, -1):
        p.append(0.7 * 2/(n * (n+1)) * i)
    return np.random.choice(n+1, 1, p=p)[0]

def Ps(n):
    return np.random.randint(0, n)

def S(words):
    re_word_1 = ["aSa", "bSb", "cSc", "dSd"]
    re_word_2 = ["aa", "bb", "cc", "dd", "a", "b", "c", "d"]
    if(Pb(len(words.replace("S", ""))) == 0):
        return S(words.replace("S", re_word_1[Ps(4)], 1))
    else:
        return words.replace("S", re_word_2[Ps(8)], 1)

def error(words, label):
    vocb = dict(a="1", b="2", c="3", d="4")
    l = int(len(words)/2)
    if l is not 0:
        mpoint = len(words) - l
        pe = Pe(l)
        nerror = random.sample(range(mpoint, len(words)), pe if pe <= 4 else 4)
        for i in nerror:
            s = ["a", "b", "c", "d"]
            s.remove(words[i])
            label[i] = vocb.get(words[i])
            words[i] = random.choice(s)
    return "".join(words), "".join(label)

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
    global N
    f = open("grammar_data.txt", 'w')
    words_list = []
    while(True):
        rb = random.uniform(0.9, 0.98)
        printProgress(len(words_list), 100000, 'Progress', 'Complete')
        if(len(words_list) >= 100000):
            break

        words = list(S("S"))
        if len(words) > N:
            continue
        label = ["0" for i in range(len(words))]
        words, label = error(words, label)

        if words not in words_list:
            words_list.append(words)
            f.write("%s\t%s\n" % (" ".join(words), " ".join(label)))

        else:
            continue
 
if __name__ == "__main__":
    main()
