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

def S1(brackets, check):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("*S1", "B", 1)
        check = check.replace("*S1", "B", 1)
        b = BT()
        if(b == 0):
            brackets = brackets.replace("B", "[S]", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 1):
            brackets = brackets.replace("B", "{S}", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 2):
            brackets = brackets.replace("B", "[S}", 1)
            check = check.replace("B", "0S1", 1)
        elif(b == 3):
            brackets = brackets.replace("B", "{S]", 1)
            check = check.replace("B", "0S2", 1)
    else:
        brackets = brackets.replace("*S1", "T", 1)
        check = check.replace("*S1", "T", 1)
        t = BT()
        if(t == 0):
            brackets = brackets.replace("T", "[]", 1)
            check = check.replace("T", "00", 1)
        elif(t == 1):
            brackets = brackets.replace("T", "{}", 1)
            check = check.replace("T", "00", 1)
        elif(t == 2):
            brackets = brackets.replace("T", "[}", 1)
            check = check.replace("T", "01", 1)
        elif(t == 3):
            brackets = brackets.replace("T", "{]", 1)
            check = check.replace("T", "02", 1)
 
    return brackets, check
 
def S(brackets, check):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))
 
    if(Pc(l) == 0):
        brackets = brackets.replace("*S", "S1S", 1)
        check = check.replace("*S", "S1S", 1)
    else:
        brackets = brackets.replace("*S", "S1", 1)
        check = check.replace("*S", "S1", 1)

    return brackets, check

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
        rb = random.uniform(0.6, 0.8)
        rc = random.uniform(0.3, 0.6)
        printProgress(len(brackets_list), 100000, 'Progress', 'Complete')
        if(len(brackets_list) >= 100000):
            break
        result = "*S"
        check = "*S"
        sequence = []
        num = 0

        while(True):
            if "*" not in result:
                break
            elif "*S1" in result:
                point = result.find('*S1')
                result, check = S1(result, check)
                if(result.find('S', point + 1) != -1):
                    result = result.replace(result[result.find('S', point + 1)], "*S", 1)
                    check = check.replace(check[check.find('S', point + 1)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)
                    check = check.replace("S", "*S", 1)
            elif "*S" in result:
                point = result.find('*S')
                result, check = S(result, check)
                if(result.find('S', point + 2) != -1):
                    result = result.replace(result[result.find('S', point + 1)], "*S", 1)
                    check = check.replace(check[check.find('S', point + 1)], "*S", 1)
                else:
                    result = result.replace("S", "*S", 1)
                    check = check.replace("S", "*S", 1)

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= N else N]
            check = check[:len(check) if len(check) <= N else N]
            f.write("%s\t%s\n" % (" ".join(result), " ".join(check)))

        else:
            continue

if __name__ == "__main__":
    main()
