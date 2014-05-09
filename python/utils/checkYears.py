f = open("../txt/movies.txt", 'r')

for z,line in enumerate(f):
    values = line.split('|')

    ident = values[0]
    if ident in [str(267),str(1358),str(1359)]:
        continue
    title = values[1]
    year = values[2]
    imdb = values[3]
    genre = values[4:]

    print int(year)

    print (title)
    print z+1
