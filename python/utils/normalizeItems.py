import requests
import simplejson
from rottentomatoes import RT
import imdb


# create a single node
def normalizeItemsFile(filename):

    ia = imdb.IMDb()

    f = open(filename, 'r')
    l = open('txt/finalfile.txt', 'w')
    for z, line in enumerate(f):
        print z
        values = line.split('|')

        ident = values[0]

        if ident == '267':
            print >>l, '267|unknown||||1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
            continue

        title = values[1]
        date = values[1][values[1].index('(')+1:values[1].index(')')]
        imdB = values[4]
        genre = values[5:]

        r = requests.get(imdB)

        splited = r.url.split('/')

        imdbID = splited[-2].replace('t','')

        if imdbID == 'www.imdb.com':

            results = ia.search_movie(title)
            mv = results[0] #First result

            splited = ia.get_imdbURL(mv).split('/')

            imdbID = splited[-2].replace('t','')


        final = ident + '|' + title + '|' + date + '|' + imdbID + '|'.join(genre)

        print >>l, final,

    f.close()
    l.close()



if __name__ == "__main__":
    normalizeItemsFile('ml-100k/u.item')