import random
import numpy as np
N = 100
num = 1

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

def S1(brackets, sequence):
    global num
    l = len(brackets.replace("S1", "").replace("S",""))

    if(Pb(l) == 0):
        brackets = brackets.replace("S1", "B", 1)
        sequence = sequence.replace("K", "B", 1)
        if(BT() == 0):
            brackets = brackets.replace("B", "[S]", 1)
            sequence = sequence.replace("B", str(num) + "S" + str(num), 1)
            num = num + 1
            brackets, sequence = S(brackets, sequence)
        else:
            brackets = brackets.replace("B", "{S}", 1)
            sequence = sequence.replace("B", str(num) + "S" + str(num), 1)
            num = num + 1
            brackets, sequence = S(brackets, sequence)
    else:
        brackets = brackets.replace("S1", "T", 1)
        sequence = sequence.replace("K", "T", 1)
        if (BT() == 0):
            brackets = brackets.replace("T", "[]", 1)
            sequence = sequence.replace("T", str(num) + str(num), 1)
            num = num + 1
        else:
            brackets = brackets.replace("T", "{}", 1)
            sequence = sequence.replace("T", str(num) + str(num), 1)
            num = num + 1
 
    return brackets, sequence
 
def S(brackets, sequence):
    global num
    l = len(brackets.replace("S1", "").replace("S",""))
 
    if(Pc(l) == 0):
        brackets = brackets.replace("S", "S1S", 1)
        sequence = sequence.replace("S", "KS", 1)
        brackets, sequence = S1(brackets, sequence)
        return S(brackets, sequence)
    else:
        brackets = brackets.replace("S", "S1", 1)
        sequence = sequence.replace("S", "K", 1)
        return S1(brackets, sequence)
 
def main():
    for i in range(100):
        global num
        num = 1
        brackets = "S"
        sequence = "S"

        result, seq = S(brackets, sequence)
        #print(len(result))
        result = result[:len(result) if len(result) <= 100 else 100]
        print(result)
        print(seq)
 
if __name__ == "__main__":
    main()
