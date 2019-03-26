import random
import numpy as np
import sys
N = 100
rb = 1
rc = 1

def s(l):
    global N
    return min(1, -1 * l / N + 1 if l <= N else 0.0)
 
def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc(l):
    global rc
    pc = rc * s(l)
    return np.random.choice(2, 1, p=[pc, 1 - pc])

def BT():
    return np.random.choice(36, 1, p=[0.1333, 0.1333, 0.1333, 0.1333,
                                      0.1333, 0.1333, 0.006673, 0.006673,
                                      0.006673, 0.006673, 0.006673, 0.006674,
                                      0.006673, 0.006673, 0.006673, 0.006674,
                                      0.006673, 0.006673, 0.006673, 0.006674,
                                      0.006673, 0.006673, 0.006673, 0.006674,
                                      0.006673, 0.006673, 0.006674, 0.006674,
                                      0.006673, 0.006673, 0.006674, 0.006674,
                                      0.006673, 0.006673, 0.006674, 0.006674])

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
            brackets = brackets.replace("B", "(S)", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 3):
            brackets = brackets.replace("B", "<S>", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 4):
            brackets = brackets.replace("B", "qSw", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 5):
            brackets = brackets.replace("B", "aSs", 1)
            check = check.replace("B", "0S0", 1)
        elif(b == 6):
            brackets = brackets.replace("B", "[S}", 1)
            check = check.replace("B", "0S3", 1)
        elif(b == 7):
            brackets = brackets.replace("B", "[S)", 1)
            check = check.replace("B", "0S4", 1)
        elif(b == 8):
            brackets = brackets.replace("B", "[S>", 1)
            check = check.replace("B", "0S5", 1)
        elif(b == 9):
            brackets = brackets.replace("B", "[Sw", 1)
            check = check.replace("B", "0S6", 1)
        elif(b == 10):
            brackets = brackets.replace("B", "[Ss", 1)
            check = check.replace("B", "0S7", 1)
        elif(b == 11):
            brackets = brackets.replace("B", "{S]", 1)
            check = check.replace("B", "0S8", 1)
        elif(b == 12):
            brackets = brackets.replace("B", "{S)", 1)
            check = check.replace("B", "0S9", 1)
        elif(b == 13):
            brackets = brackets.replace("B", "{S>", 1)
            check = check.replace("B", "0Sa", 1)
        elif(b == 14):
            brackets = brackets.replace("B", "{Sw", 1)
            check = check.replace("B", "0Sb", 1)
        elif(b == 15):
            brackets = brackets.replace("B", "{Ss", 1)
            check = check.replace("B", "0Sc", 1)
        elif(b == 16):
            brackets = brackets.replace("B", "(S}", 1)
            check = check.replace("B", "0Sd", 1)
        elif(b == 17):
            brackets = brackets.replace("B", "(S]", 1)
            check = check.replace("B", "0Se", 1)
        elif(b == 18):
            brackets = brackets.replace("B", "(S>", 1)
            check = check.replace("B", "0Sf", 1)
        elif(b == 19):
            brackets = brackets.replace("B", "(Sw", 1)
            check = check.replace("B", "0Sg", 1)
        elif(b == 20):
            brackets = brackets.replace("B", "(Ss", 1)
            check = check.replace("B", "0Sh", 1)
        elif(b == 21):
            brackets = brackets.replace("B", "<S}", 1)
            check = check.replace("B", "0Si", 1)
        elif(b == 22):
            brackets = brackets.replace("B", "<S]", 1)
            check = check.replace("B", "0Sj", 1)
        elif(b == 23):
            brackets = brackets.replace("B", "<S)", 1)
            check = check.replace("B", "0Sk", 1)
        elif(b == 24):
            brackets = brackets.replace("B", "<Sw", 1)
            check = check.replace("B", "0Sl", 1)
        elif(b == 25):
            brackets = brackets.replace("B", "<Ss", 1)
            check = check.replace("B", "0Sm", 1)
        elif(b == 26):
            brackets = brackets.replace("B", "qS}", 1)
            check = check.replace("B", "0Sn", 1)
        elif(b == 27):
            brackets = brackets.replace("B", "qS]", 1)
            check = check.replace("B", "0So", 1)
        elif(b == 28):
            brackets = brackets.replace("B", "qS)", 1)
            check = check.replace("B", "0Sp", 1)
        elif(b == 29):
            brackets = brackets.replace("B", "qS>", 1)
            check = check.replace("B", "0Sq", 1)
        elif(b == 30):
            brackets = brackets.replace("B", "qSs", 1)
            check = check.replace("B", "0Sr", 1)
        elif(b == 31):
            brackets = brackets.replace("B", "aS}", 1)
            check = check.replace("B", "0Ss", 1)
        elif(b == 32):
            brackets = brackets.replace("B", "aS]", 1)
            check = check.replace("B", "0St", 1)
        elif(b == 33):
            brackets = brackets.replace("B", "aS)", 1)
            check = check.replace("B", "0Su", 1)
        elif(b == 34):
            brackets = brackets.replace("B", "aSw", 1)
            check = check.replace("B", "0S1", 1)
        elif(b == 35):
            brackets = brackets.replace("B", "aS>", 1)
            check = check.replace("B", "0S2", 1)
    else:
        brackets = brackets.replace("*S1", "T", 1)
        check = check.replace("*S1", "T", 1)
        b = BT()
        if(b == 0):
            brackets = brackets.replace("T", "[]", 1)
            check = check.replace("T", "00", 1)
        elif(b == 1):
            brackets = brackets.replace("T", "{}", 1)
            check = check.replace("T", "00", 1)
        elif(b == 2):
            brackets = brackets.replace("T", "()", 1)
            check = check.replace("T", "00", 1)
        elif(b == 3):
            brackets = brackets.replace("T", "<>", 1)
            check = check.replace("T", "00", 1)
        elif(b == 4):
            brackets = brackets.replace("T", "qw", 1)
            check = check.replace("T", "00", 1)
        elif(b == 5):
            brackets = brackets.replace("T", "as", 1)
            check = check.replace("T", "00", 1)
        elif(b == 6):
            brackets = brackets.replace("T", "[}", 1)
            check = check.replace("T", "03", 1)
        elif(b == 7):
            brackets = brackets.replace("T", "[)", 1)
            check = check.replace("T", "04", 1)
        elif(b == 8):
            brackets = brackets.replace("T", "[>", 1)
            check = check.replace("T", "05", 1)
        elif(b == 9):
            brackets = brackets.replace("T", "[w", 1)
            check = check.replace("T", "06", 1)
        elif(b == 10):
            brackets = brackets.replace("T", "[s", 1)
            check = check.replace("T", "07", 1)
        elif(b == 11):
            brackets = brackets.replace("T", "{]", 1)
            check = check.replace("T", "08", 1)
        elif(b == 12):
            brackets = brackets.replace("T", "{)", 1)
            check = check.replace("T", "09", 1)
        elif(b == 13):
            brackets = brackets.replace("T", "{>", 1)
            check = check.replace("T", "0a", 1)
        elif(b == 14):
            brackets = brackets.replace("T", "{w", 1)
            check = check.replace("T", "0b", 1)
        elif(b == 15):
            brackets = brackets.replace("T", "{s", 1)
            check = check.replace("T", "0c", 1)
        elif(b == 16):
            brackets = brackets.replace("T", "(}", 1)
            check = check.replace("T", "0d", 1)
        elif(b == 17):
            brackets = brackets.replace("T", "(]", 1)
            check = check.replace("T", "0e", 1)
        elif(b == 18):
            brackets = brackets.replace("T", "(>", 1)
            check = check.replace("T", "0f", 1)
        elif(b == 19):
            brackets = brackets.replace("T", "(w", 1)
            check = check.replace("T", "0g", 1)
        elif(b == 20):
            brackets = brackets.replace("T", "(s", 1)
            check = check.replace("T", "0h", 1)
        elif(b == 21):
            brackets = brackets.replace("T", "<}", 1)
            check = check.replace("T", "0i", 1)
        elif(b == 22):
            brackets = brackets.replace("T", "<]", 1)
            check = check.replace("T", "0j", 1)
        elif(b == 23):
            brackets = brackets.replace("T", "<)", 1)
            check = check.replace("T", "0k", 1)
        elif(b == 24):
            brackets = brackets.replace("T", "<w", 1)
            check = check.replace("T", "0l", 1)
        elif(b == 25):
            brackets = brackets.replace("T", "<s", 1)
            check = check.replace("T", "0m", 1)
        elif(b == 26):
            brackets = brackets.replace("T", "q}", 1)
            check = check.replace("T", "0n", 1)
        elif(b == 27):
            brackets = brackets.replace("T", "q]", 1)
            check = check.replace("T", "0o", 1)
        elif(b == 28):
            brackets = brackets.replace("T", "q)", 1)
            check = check.replace("T", "0p", 1)
        elif(b == 29):
            brackets = brackets.replace("T", "q>", 1)
            check = check.replace("T", "0q", 1)
        elif(b == 30):
            brackets = brackets.replace("T", "qs", 1)
            check = check.replace("T", "0r", 1)
        elif(b == 31):
            brackets = brackets.replace("T", "a}", 1)
            check = check.replace("T", "0s", 1)
        elif(b == 32):
            brackets = brackets.replace("T", "a]", 1)
            check = check.replace("T", "0t", 1)
        elif(b == 33):
            brackets = brackets.replace("T", "a)", 1)
            check = check.replace("T", "0u", 1)
        elif(b == 34):
            brackets = brackets.replace("T", "aw", 1)
            check = check.replace("T", "01", 1)
        elif(b == 35):
            brackets = brackets.replace("T", "a>", 1)
            check = check.replace("T", "01", 1)

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
    iterator = 10000
    for i in range(0,iterator):
        rb = random.uniform(0.7, 0.9)
        rc = random.uniform(0.4, 0.8)
        printProgress(i, iterator, 'Progress', 'Complete')
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

        result = result[:len(result) if len(result) <= N else N]
        check = check[:len(check) if len(check) <= N else N]
        check_int = " ".join(check)
        check_int = (check_int.replace("a", "10").replace("b", "11").replace("c", "12")
                                 .replace("d", "13").replace("e", "14").replace("f", "15")
                                 .replace("g", "16").replace("h", "17").replace("i", "18")
                                 .replace("j", "19").replace("k", "20").replace("l", "21")
                                 .replace("m", "22").replace("n", "23").replace("o", "24")
                                 .replace("p", "25").replace("q", "26").replace("r", "27")
                                 .replace("s", "28").replace("t", "29").replace("u", "30"))
        f.write("%s\t%s\n" % (" ".join(result), check_int))

if __name__ == "__main__":
    main()
