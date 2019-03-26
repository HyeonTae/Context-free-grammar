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

def Pc(l):
    global rc
    if(l >= 5):
        rc = 0
    return np.random.choice(2, 1, p=[rc, 1 - rc])

def Pe():
    return np.random.choice(10, 1, p=[0.1, 0.1, 0.1, 0.1, 0.1,
                                      0.1, 0.1, 0.1, 0.1, 0.1])

def Ps1():
    return np.random.choice(5, 1, p=[0.2, 0.2, 0.2, 0.2, 0.2])

def Ps2():
    return np.random.choice(10, 1, p=[0.1, 0.1, 0.1, 0.1, 0.1,
                                      0.1, 0.1, 0.1, 0.1, 0.1])

def S(words, label):
    l = len(words.replace("S", "").replace("*", "").replace("#", ""))

    if(Pb(l) == 0):
        return S1(words, label)
    else:
        return S2(words, label)

def S1(words, label):
    ps1=Ps1()
    if(ps1 == 0):
        words = words.replace("*S", "aSa", 1)
    elif(ps1 == 1):
        words = words.replace("*S", "bSb", 1)
    elif(ps1 == 2):
        words = words.replace("*S", "cSc", 1)
    elif(ps1 == 3):
        words = words.replace("*S", "dSd", 1)
    else:
        words = words.replace("*S", "eSe", 1)

    label = label.replace("*S", "0S0", 1)
    return words, label

def S2(words, label):
    ps2=Ps2()
    if(ps2 == 0):
        words = words.replace("*S", "aa", 1)
        label = label.replace("*S", "00", 1)
    elif(ps2 == 1):
        words = words.replace("*S", "bb", 1)
        label = label.replace("*S", "00", 1)
    elif(ps2 == 2):
        words = words.replace("*S", "cc", 1)
        label = label.replace("*S", "00", 1)
    elif(ps2 == 3):
        words = words.replace("*S", "dd", 1)
        label = label.replace("*S", "00", 1)
    elif(ps2 == 4):
        words = words.replace("*S", "ee", 1)
        label = label.replace("*S", "00", 1)
    elif(ps2 == 5):
        words = words.replace("*S", "a", 1)
        label = label.replace("*S", "0", 1)
    elif(ps2 == 6):
        words = words.replace("*S", "b", 1)
        label = label.replace("*S", "0", 1)
    elif(ps2 == 7):
        words = words.replace("*S", "c", 1)
        label = label.replace("*S", "0", 1)
    elif(ps2 == 8):
        words = words.replace("*S", "d", 1)
        label = label.replace("*S", "0", 1)
    else:
        words = words.replace("*S", "e", 1)
        label = label.replace("*S", "0", 1)

    return words, label

def SS(words, label):
    l = len(words.replace("*", "").replace("#", ""))

    if(Pc(l) == 0):
        return SS(words + "#S", label + "#S")
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
    brackets_list = []
    while(True):
        rb = random.uniform(0.9, 0.95)
        rc = random.uniform(0.4, 0.6)
        printProgress(len(brackets_list), 100000, 'Progress', 'Complete')
        if(len(brackets_list) >= 100000):
            break
        words = "#*S"
        label = "#*S"
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
                    result = result[:result.find('S', point + 2)] + "*S" + result[result.find('S', point + 2)+1:]
                    label = label[:label.find('S', point + 2)] + "*S" + label[label.find('S', point + 2)+1:]
                else:
                    result = result.replace("S", "*S", 1)
                    label = label.replace("S", "*S", 1)

        point_2 = 0
        for i in range(result.count('#')):
            point_1 = point_2
            point_2 = len(result) if result.find('#', point_1 + 1) == -1 else result.find('#', point_1 + 1)
            if point_2 - point_1 == 2:
                continue
            mpoint = int(point_2 - (point_2-point_1)/2) + 1
            rand_input = random.randrange(mpoint, point_2)
            pe=Pe()
            if(result[rand_input] == "a"):
                result = result[:rand_input] + "*" + result[rand_input+1:]
                label = label[:rand_input] + "*" + label[rand_input+1:]
                if(pe == 0):
                    result = result.replace("*", "b", 1)
                    label = label.replace("*", "1", 1)
                elif(pe == 1):
                    result = result.replace("*", "c", 1)
                    label = label.replace("*", "1", 1)
                elif(pe == 2):
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "1", 1)
                elif(pe == 3):
                    result = result.replace("*", "e", 1)
                    label = label.replace("*", "1", 1)
                else:
                    result = result.replace("*", "a", 1)
                    label = label.replace("*", "0", 1)
            elif(result[rand_input] == "b"):
                result = result[:rand_input] + "*" + result[rand_input+1:]
                label = label[:rand_input] + "*" + label[rand_input+1:]
                if(pe == 0):
                    result = result.replace("*", "a", 1)
                    label = label.replace("*", "2", 1)
                elif(pe == 1):
                    result = result.replace("*", "c", 1)
                    label = label.replace("*", "2", 1)
                elif(pe == 2):
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "2", 1)
                elif(pe == 3):
                    result = result.replace("*", "e", 1)
                    label = label.replace("*", "2", 1)
                else:
                    result = result.replace("*", "b", 1)
                    label = label.replace("*", "0", 1)
            elif(result[rand_input] == "c"):
                result = result[:rand_input] + "*" + result[rand_input+1:]
                label = label[:rand_input] + "*" + label[rand_input+1:]
                if(pe == 0):
                    result = result.replace("*", "a", 1)
                    label = label.replace("*", "3", 1)
                elif(pe == 1):
                    result = result.replace("*", "b", 1)
                    label = label.replace("*", "3", 1)
                elif(pe == 2):
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "3", 1)
                elif(pe == 3):
                    result = result.replace("*", "e", 1)
                    label = label.replace("*", "3", 1)
                else:
                    result = result.replace("*", "c", 1)
                    label = label.replace("*", "0", 1)
            elif(result[rand_input] == "d"):
                result = result[:rand_input] + "*" + result[rand_input+1:]
                label = label[:rand_input] + "*" + label[rand_input+1:]
                if(pe == 0):
                    result = result.replace("*", "a", 1)
                    label = label.replace("*", "4", 1)
                elif(pe == 1):
                    result = result.replace("*", "b", 1)
                    label = label.replace("*", "4", 1)
                elif(pe == 2):
                    result = result.replace("*", "c", 1)
                    label = label.replace("*", "4", 1)
                elif(pe == 3):
                    result = result.replace("*", "e", 1)
                    label = label.replace("*", "4", 1)
                else:
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "0", 1)
            elif(result[rand_input] == "e"):
                result = result[:rand_input] + "*" + result[rand_input+1:]
                label = label[:rand_input] + "*" + label[rand_input+1:]
                if(pe == 0):
                    result = result.replace("*", "a", 1)
                    label = label.replace("*", "5", 1)
                elif(pe == 1):
                    result = result.replace("*", "b", 1)
                    label = label.replace("*", "5", 1)
                elif(pe == 2):
                    result = result.replace("*", "c", 1)
                    label = label.replace("*", "5", 1)
                elif(pe == 3):
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "5", 1)
                else:
                    result = result.replace("*", "e", 1)
                    label = label.replace("*", "0", 1)
        

        result = result.replace("#", "")
        label = label.replace("#", "")
        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            label = label[:len(label) if len(label) <= N else N]
            f.write("%s\t%s\n" % (" ".join(result), " ".join(label)))

        else:
            continue
 
if __name__ == "__main__":
    main()
