import random
import numpy as np
import sys
N = 50
rb = 1
rc = 1

def s(l):
    return min(1, -3 * l / N + 3 if l <= 50 else 0.0)
 
def Pb(l):
    global rb
    #rb = random.uniform(0.4, 0.8)
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    global rc
    #rc = random.uniform(0.4, 0.8)
    pc = rc * s(l)
    return np.random.choice(2, 1, p=[pc, 1 - pc])

def BT():
    return np.random.choice(2, 1, p=[0.5, 0.5])

def S1(brackets):
    l = len(brackets.replace("S1", "").replace("S","").replace("*",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("*S1", "B", 1)
        if(BT() == 0):
            brackets = brackets.replace("B", "[S]", 1)
        else:
            brackets = brackets.replace("B", "{S}", 1)
    else:
        brackets = brackets.replace("*S1", "T", 1)
        if (BT() == 0):
            brackets = brackets.replace("T", "[]", 1)
        else:
            brackets = brackets.replace("T", "{}", 1)
 
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

def main():
    global rb
    global rc
    f = open("grammar_data_50.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.4, 0.8)
        rc = random.uniform(0.4, 0.8)
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
            #print(len(result))
            result = result[:len(result) if len(result) <= 50 else 50]
            for i in result:
                if(i == "{" or i == "["):
                    num = num + 1
                    sequence.append(str(num))
                elif(i == "}" or i == "]"):
                    num = num - 1
                    sequence.append(str(num))
            f.write("%s\t%s\n" % (" ".join(result), " ".join(sequence)))

            #print(result)
            #print(sequence)
        else:
            continue
 
if __name__ == "__main__":
    main()
