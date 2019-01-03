ttt = "{[S1]*S}[]S[S1]"

print(ttt)
a = ttt.find('*S')

b = ttt.find('S', a+1)

d = ttt.replace(ttt[b], "*S", 1)
print(d)
