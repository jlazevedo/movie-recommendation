import re
from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

genres = []

# create a single node
def createNodesfromMovieFile(filename):

    z = 1

    aux = 0

    genrs_array = []

    nodes = []

    array = []

    with open(filename, 'r') as f1, open('images.txt', 'r') as f2, open('adjectives.txt', 'r') as f3, open('descriptions.txt', 'r') as f4 :
        for x, y, d, o in zip(f1, f2, f3, f4):

            print x,

            q = re.sub('[\n [\]\']', '', d).split(',')

            if len(q) == 1 and q[0] == '':
                q = []

            print q
            array.append(q)

            #print z
            values = x.split('|')

            ident = values[0]
            title = values[1]
            try:
                year = int(values[2])
            except ValueError, e:
                year = None
            imdb = values[3]
            genre = values[4:]
            movie_genres = []
            img = y[:-1]

            movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', ident,
                    node({'movie_id': ident, 'title': unicode(title, errors='ignore'),
                          'imdb': imdb, 'img': img, 'year': year, 'description': unicode(o.replace('\n',''),errors='ignore')}))

            for i, n in enumerate(map(int, genre)):
                if n == 1:
                    movie_genres.append((i, batch.get_or_create_in_index(neo4j.Node, 'Genre', 'genre_id', i, node({'genre_id': int(i), 'name': genres[i]}))))
                    aux += 1


            for gen_id, gen in movie_genres:
                batch.get_or_create_in_index(neo4j.Relationship, 'Genre_As', 'genre_as', ident+str(gen_id), rel(movie, 'Genre_As', gen))
                aux += 1
            genrs_array.append(aux)
            aux = 0

            if z % 200 == 0:
                nodes += batch.submit()
                batch.clear()

            z += 1

        w = 0

        print len(array)

        for e, n in enumerate(nodes):
            if e == 0:
                print n
                for a in array[w]:
                    batch.add_labels(n, a)
                w += 1
            elif genrs_array[0] == 0:
                print n
                for a in array[w]:
                    batch.add_labels(n, a)
                genrs_array = genrs_array[1:]
                w += 1
            else:
                print -1
                genrs_array[0] -= 1

    batch.submit()

    print "ENDED"

    

    

def createGenres(filename):
    f = open(filename, 'r')
    for line in f:
        genre, ident = line.split('|')
        genres.append(genre)
    
    f.close()
    
    
    
if __name__ == "__main__":
    createGenres('ml-100k/u.genre')
    createNodesfromMovieFile('finalfile2.txt')