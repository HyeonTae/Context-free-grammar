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
    pc = rc * s(l)
    return np.random.choice(2, 1, p=[pc, 1 - pc])

def BT():
    return np.random.choice(4, 1, p=[0.4, 0.4, 0.1, 0.1])

def S1(brackets):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("*S1", "B", 1)
        b = BT()
        if(b == 0):
            brackets = brackets.replace("B", "[S]", 1)
        elif(b == 1):
            brackets = brackets.replace("B", "{S}", 1)
        elif(b == 2):
            brackets = brackets.replace("B", "[S}", 1)
        elif(b == 3):
            brackets = brackets.replace("B", "{S]", 1)
    else:
        brackets = brackets.replace("*S1", "T", 1)
        t = BT()
        if(t == 0):
            brackets = brackets.replace("T", "[]", 1)
        elif(t == 1):
            brackets = brackets.replace("T", "{}", 1)
        elif(t == 2):
            brackets = brackets.replace("T", "[}", 1)
        elif(t == 3):
            brackets = brackets.replace("T", "{]", 1)
 
    return brackets
 
def S(brackets):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))
 
    if(Pc(l) == 0):
        brackets = brackets.replace("*S", "S1S", 1)
    else:
        brackets = brackets.replace("*S", "S1", 1)

    return brackets

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 50):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
    if(iteration == total):
        sys.stdout.write('\n')
    sys.stdout.flush()

def labeling(data):
    result = []
    check = []
    num = 0
    for i in data:
        num += 1
        if i == "}":
            if check.pop() == "[":
                result.append(str(num)+"a")
        elif i == "]":
            if check.pop() == "{":
                result.append(str(num)+"b")
        else:
            check.append(i)
    if not result:
        result.append(str(0))
    return " ".join(result)

def main():
    global rb
    global rc
    global N
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.6, 0.8)
        rc = random.uniform(0.3, 0.6)
        printProgress(len(brackets_list), 100000, 'Progress', 'Complete')
        if(len(brackets_list) >= 100000):
            break
        result = "*S"
        sequence = []
        num = 0

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
                    result = result.replace(result[result.find('S', point + 1)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            label = labeling(result)
            f.write("%s\t%s\n" % (" ".join(result), label))

        else:
            continue

if __name__ == "__main__":
    main()
