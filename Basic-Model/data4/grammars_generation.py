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
    l = len(brackets.replace("S1", "").replace("S",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("S1", "B", 1)
        if(BT() == 0):
            brackets = brackets.replace("B", "[S]", 1)
            brackets = S(brackets)
        else:
            brackets = brackets.replace("B", "{S}", 1)
            brackets = S(brackets)
    else:
        brackets = brackets.replace("S1", "T", 1)
        if (BT() == 0):
            brackets = brackets.replace("T", "[]", 1)
        else:
            brackets = brackets.replace("T", "{}", 1)
 
    return brackets
 
def S(brackets):
    l = len(brackets.replace("S1", "").replace("S",""))
 
    if(Pc(l) == 0):
        brackets = brackets.replace("S", "S1S", 1)
        brackets = S1(brackets)
        return S(brackets)
    else:
        brackets = brackets.replace("S", "S1", 1)
        return S1(brackets)

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
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.4, 0.8)
        rc = random.uniform(0.4, 0.8)
        printProgress(len(brackets_list), 10000, 'Progress', 'Complete')
        if(len(brackets_list) >= 10000):
            break
        brackets = "S"
        sequence = []
        num = 0

        result = S(brackets)

        if result not in brackets_list:
            brackets_list.append(result)
            #print(len(result))
            result = result[:len(result) if len(result) <= 100 else 100]
            for i in result:
                if(i == "{" or i == "["):
                    num = num + 1
                    sequence.append(str(num))
                elif(i == "}" or i == "]"):
                    num = num - 1
                    sequence.append(str(num))
            f.write("%s\t%s\n" % (result, ",".join(sequence)))

            #print(result)
            #print(sequence)
        else:
            continue
 
if __name__ == "__main__":
    main()
