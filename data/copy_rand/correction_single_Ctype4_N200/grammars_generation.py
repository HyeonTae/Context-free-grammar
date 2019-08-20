import random
import numpy as np
import sys

N = 200
rb = 1

def s(l):
    return min(1, - 2 * l / N + 2.5 if l <= N else 0.0)

def Pb(l):
    global rb
    pb = rb * s(l)
    return np.random.choice(2, 1, p=[pb, 1 - pb])

def Pc():
    return np.random.choice(4, 1, p=[0.25, 0.25, 0.25, 0.25])

def Pe():
    return np.random.choice(4, 1, p=[0.2333, 0.2333, 0.2334, 0.3])

def S(words):
    l = len(words.replace("S", ""))
    pb = Pb(l)
    if(pb == 0):
        pc = Pc()
        if pc == 0:
            words = words.replace("S", "aS", 1)
        elif pc == 1:
            words = words.replace("S", "bS", 1)
        elif pc == 2:
            words = words.replace("S", "cS", 1)
        else:
            words = words.replace("S", "dS", 1)

        return S(words)
    else:
        pc = Pc()
        if pc == 0:
            words = words.replace("S", "a", 1)
        elif pc == 1:
            words = words.replace("S", "b", 1)
        elif pc == 2:
            words = words.replace("S", "c", 1)
        else:
            words = words.replace("S", "d", 1)

        return words

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
    f = open("grammar_data.txt", 'w')
    brackets_list = []
    while(True):
        rb = random.uniform(0.9, 0.98)
        printProgress(len(brackets_list), 50000, 'Progress', 'Complete')
        if(len(brackets_list) >= 50000):
            break

        words = "S"
        label = ""
        result = S(words)
        result += result
        for i in result:
            label += "0"

        if len(result) > N or len(result) < 101:
            continue

        mpoint = len(result) - int(len(result)/2)
        if len(result) != 1:
            rand_input = random.randrange(mpoint, len(result))
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
                else:
                    result = result.replace("*", "d", 1)
                    label = label.replace("*", "0", 1)

        if result not in brackets_list:
            brackets_list.append(result)

            f.write("%s\t%s\n" % (" ".join(result), " ".join(label)))
        else:
            continue

if __name__ == "__main__":
    main()
