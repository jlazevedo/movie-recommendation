import requests
import simplejson
from rottentomatoes import RT
import imdb


# create a single node
def imdbDescriptions(filename):

    ia = imdb.IMDb()

    f = open(filename, 'r')
    l = open('../txt/descriptions.txt', 'a')
    for z, line in enumerate(f):
        print z
        values = line.split('|')

        imdbID = values[3]

        try:
            x = ia.get_movie(imdbID)['plot outline']
            print x


            print >>l, x.encode('utf-8').strip()

        except KeyError, e:
            print >>l, ''



    f.close()
    l.close()



if __name__ == "__main__":
    imdbDescriptions('../txt/movies.txt')