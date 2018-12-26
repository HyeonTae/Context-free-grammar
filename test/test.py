import random
import numpy as np
N = 100
 
def s(l):
    return min(1, -3 * l / N + 3)
 
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

def K(brackets):
    l = len(brackets.replace("K", "").replace("S",""))
    if(l >= N):
        return brackets

    if(Pb(l) == 0):
        brackets = brackets.replace("K", "B", 1)
        if(BT() == 0):
            brackets = brackets.replace("B", "[S]", 1)
            brackets = S(brackets)
        else:
            brackets = brackets.replace("B", "{S}", 1)
            brackets = S(brackets)
    else:
        brackets = brackets.replace("K", "T", 1)
        if (BT() == 0):
            brackets = brackets.replace("T", "[]", 1)
        else:
            brackets = brackets.replace("T", "{}", 1)
 
    return brackets
 
def S(brackets):
    l = len(brackets.replace("K", "").replace("S",""))
    if (l >= N):
        return brackets
 
    if(Pc(l) == 0):
        brackets = brackets.replace("S", "KS", 1)
        brackets = K(brackets)
        return S(brackets)
    else:
        brackets = brackets.replace("S", "K", 1)
        return K(brackets)
 
def main():
    for i in range(10):
        brackets = "S"

        result = S(brackets)
        print(len(result))
        print(result)
 
if __name__ == "__main__":
    main()
