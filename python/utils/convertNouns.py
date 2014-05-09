import re
f = open("../txt/adjectives.txt", 'r')
for z,line in enumerate(f):
    line= re.sub('[.!,;]', '', line)
