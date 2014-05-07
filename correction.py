

f = open('finalfile.txt', 'r')
l = open('finalfile2.txt', 'w')

for line in f:
    values = line.split('|')

    print >>l, '|'.join(values[:3]) + '|' + values[3][:-1] + '|' + values[3][-1:] + '|' + '|'.join(values[4:]),