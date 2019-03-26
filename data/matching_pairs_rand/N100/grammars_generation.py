import random
import numpy as np
import sys
N = 100
rb = 1
rc = 1

def s(l):
    global N
    return min(1, -1.5 * l / N + 1.5 if l <= N else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    global rc
    if(l >= 15):
        rc = 0
    return np.random.choice(2, 1, p=[rc, 1 - rc])

def S(words):
    l = len(words.replace("S1", "").replace("S", "").replace("*", ""))

    if(Pb(l) == 0):
        return words.replace("*S", "aSb", 1)
    else:
        return words.replace("*S", "ab", 1)

def S1(words):
    l = len(words.replace("S1", "").replace("S", "").replace("*", ""))

    if(Pb(l) == 0):
        return words.replace("*S1", "bS1a", 1)
    else:
        return words.replace("*S1", "ba", 1)

def SS(words):
    l = len(words.replace("*", ""))

    if(Pc(l) == 0):
        if(words[-1:] == '1'):
            return SS(words + "S")
        else:
            return SS(words + "S1")
    else:
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
    global N
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.8, 0.9)
        rc = random.uniform(0.8, 0.9)
        printProgress(len(brackets_list), 10000, 'Progress', 'Complete')
        if(len(brackets_list) >= 10000):
            break
        result = "*S"
        sequence = []
        num = 0

        result = SS(result)

        while(True):
            if "*" not in result:
                break
            elif "*S1" in result:
                point = result.find('*S1')
                result = S1(result)
                if(result.find('S', point + 1) != -1):
                    result = result.replace(result[result.find('S', point + 1)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)
            elif "*S" in result:
                point = result.find('*S')
                result = S(result)
                if(result.find('S', point + 2) != -1):
                    result = result.replace(result[result.find('S', point + 2)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            check = True
            for i in result:
                if(check == True):
                    if(i == "a"):
                        num = num + 1
                        sequence.append(str(num))
                    elif(i == "b"):
                        num = num - 1
                        sequence.append(str(num))
                        if(num == 0):
                            check = False
                else:
                    if(i == "b"):
                        num = num + 1
                        sequence.append(str(num))
                    elif(i == "a"):
                        num = num - 1
                        sequence.append(str(num))
                        if(num == 0):
                            check = True
            f.write("%s\t%s\n" % (" ".join(result), " ".join(sequence)))

        else:
            continue
 
if __name__ == "__main__":
    main()
