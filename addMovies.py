from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

genres = []

# create a single node
def createNodesfromMovieFile(filename):
    f = open(filename, 'r');
    for line in f:
        values = line.split('|')
        
        ident = values[0]
        title = values[1]
        imdb = values[4]
        genre = values[5:]
        movie_genres = []
        
        for i, n in enumerate(map(int, genre)):
            if n == 1:
                movie_genres.append((i, batch.get_or_create_in_index(neo4j.Node, 'Genre', 'genre_id', i, node({'genre_id': int(i), 'name': genres[i]}))))
        
        movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', ident, node({'movie_id': ident, 'title': unicode(title, errors='ignore'), 'imdb': imdb}))
        
        for gen_id, gen in movie_genres:
            batch.get_or_create_in_index(neo4j.Relationship, 'Genre_As', 'genre_as', ident+str(gen_id), rel(movie, 'Genre_As', gen))
        
    
    nodes = batch.submit()
    batch.clear()
    
    print "ENDED"
    
    f.close()
    
    return nodes
    

def createGenres(filename):
    f = open(filename, 'r')
    for line in f:
        genre, ident = line.split('|')
        genres.append(genre)
    
    f.close()
    
    
    
if __name__ == "__main__":
    createGenres('ml-100k/u.genre')
    createNodesfromMovieFile('ml-100k/u.item')