import random
import numpy as np
N = 100

def s(l):
    return min(1, -3 * l / N + 3 if l <= 100 else 0.0)
 
def Pb(l):
    rb = random.uniform(0.4, 0.8)
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    rc = random.uniform(0.4, 0.8)
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
 
def main():
    f = open("ooo.txt", 'w')
    for i in range(10):
        brackets = "S"
        sequence = []
        num = 0

        result = S(brackets)
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
 
if __name__ == "__main__":
    main()
