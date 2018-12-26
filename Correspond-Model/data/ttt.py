import re

s = "{ab + 1}[b -*/3][""]['']{,./?:!~%=&|^$#@ ()  }()[]"
print(s)

p = re.sub("[a-zA-Z0-9""'',.?!/~%:=&|^$#@+*-]", "", s)
p = p.replace(" ","")

print(p)
