import random
import numpy as np
import sys
N = 70
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
    return np.random.choice(4, 1, p=[0.25, 0.25, 0.25, 0.25])

def S1(brackets):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("*S1", "B", 1)
        if(BT() == 0):
            brackets = brackets.replace("B", "[S]", 1)
        elif(BT() == 1):
            brackets = brackets.replace("B", "{S}", 1)
        elif(BT() == 2):
            brackets = brackets.replace("B", "(S)", 1)
        else:
            brackets = brackets.replace("B", "<S>", 1)
    else:
        brackets = brackets.replace("*S1", "T", 1)
        if (BT() == 0):
            brackets = brackets.replace("T", "[]", 1)
        elif (BT() == 1):
            brackets = brackets.replace("T", "{}", 1)
        elif (BT() == 2):
            brackets = brackets.replace("T", "()", 1)
        else:
            brackets = brackets.replace("T", "<>", 1)
 
    return brackets
 
def S(brackets):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))
 
    if(Pc(l) == 0):
        brackets = brackets.replace("*S", "S1S", 1)
    else:
        brackets = brackets.replace("*S", "S1", 1)

    return brackets

def nonbracket():
    n = np.random.choice(6, 1, p=[0.166, 0.167, 0.166, 0.167, 0.166, 0.168])
    if n == 0:
        return 'a'
    elif n == 1:
        return 'b'
    elif n == 2:
        return 'c'
    elif n == 3:
        return 'd'
    elif n == 4:
        return 'e'
    else:
        return 'f'

def insert_nonbracket(brackets, lenth):
    iterator = int(random.uniform(1, lenth - 1))
    for i in range(0, iterator):
        index = int(random.uniform(1, lenth))
        brackets = brackets[:index] + nonbracket() + brackets[index:]
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

def main():
    global rb
    global rc
    global N
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.6, 0.8)
        rc = random.uniform(0.3, 0.6)
        printProgress(len(brackets_list), 10000, 'Progress', 'Complete')
        if(len(brackets_list) >= 10000):
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

        if(BT() == 0):
            result = insert_nonbracket(result, len(result))
        else:
            result

        if result not in brackets_list:
            brackets_list.append(result)
            result = result[:len(result) if len(result) <= 100 else 100]
            for i in result:
                if(i == "{" or i == "[" or i == "(" or i == "<"):
                    num = num + 1
                    sequence.append(str(num))
                elif(i == "}" or i == "]" or i == ")" or i == ">"):
                    num = num - 1
                    sequence.append(str(num))
                else:
                    sequence.append(str(num))
            f.write("%s\t%s\n" % (" ".join(result), " ".join(sequence)))

        else:
            continue
 
if __name__ == "__main__":
    main()
