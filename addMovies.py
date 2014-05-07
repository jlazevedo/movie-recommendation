import requests
from rottentomatoes import RT
from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

genres = []

# create a single node
def createNodesfromMovieFile(filename):

    z = 1

    with open(filename, 'r') as f1, open('images.txt', 'r') as f2:
        for x, y in zip(f1, f2):

            print x,

            #print z
            values = x.split('|')

            ident = values[0]

            if ident == '267' or ident == '1358' or ident == '1359':
                imdb = ''


            title = values[1]
            imdb = values[3]
            genre = values[4:]
            movie_genres = []
            img = y[:-1]

            for i, n in enumerate(map(int, genre)):
                if n == 1:
                    movie_genres.append((i, batch.get_or_create_in_index(neo4j.Node, 'Genre', 'genre_id', i, node({'genre_id': int(i), 'name': genres[i]}))))

            movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', ident, node({'movie_id': ident, 'title': unicode(title, errors='ignore'), 'imdb': imdb, 'img': img}))



            for gen_id, gen in movie_genres:
                batch.get_or_create_in_index(neo4j.Relationship, 'Genre_As', 'genre_as', ident+str(gen_id), rel(movie, 'Genre_As', gen))


            if z % 50 == 0:

                nodes = batch.submit()
                batch.clear()
                print 'a'

            z += 1

        nodes = batch.submit()
        batch.clear()


    print "ENDED"

    
    return nodes
    

def createGenres(filename):
    f = open(filename, 'r')
    for line in f:
        genre, ident = line.split('|')
        genres.append(genre)
    
    f.close()
    
    
    
if __name__ == "__main__":
    createGenres('ml-100k/u.genre')
    createNodesfromMovieFile('finalfile2.txt')