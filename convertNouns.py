import re
f = open("adjectives.txt", 'r')
for z,line in enumerate(f):
    line= re.sub('[.!,;]', '', line)
