import requests
import simplejson
from rottentomatoes import RT
import imdb


# create a single node
def getJPGfromMovieFile(filename):


    ia = imdb.IMDb()


    f = open(filename, 'r')
    l = open('txt/images.txt', 'w')
    for z, line in enumerate(f):
        print z
        values = line.split('|')

        if values[1] == '267' or values[1] == '1358' or values[1] == '1359':
            print >>l, 'http://www.comicsbulletin.com/main/sites/default/files/column-covers/noCoverArt_68.gif'
            continue

        imdbID = values[3]

        request = requests.get("http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json?apikey=rh8chjzp8vu6gnpwj88736uv&type=imdb&id=" + imdbID)

        data = request.content

        js = simplejson.loads(data)

        try:
            img = js['posters'].itervalues().next()
            print >>l, img
        except KeyError, e:
            print >>l, 'http://www.comicsbulletin.com/main/sites/default/files/column-covers/noCoverArt_68.gif'


    print "ENDED"

    f.close()
    l.close()



if __name__ == "__main__":
    getJPGfromMovieFile('txt/movies.txt')