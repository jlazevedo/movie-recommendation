from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

def createNodesGenre(filename):
    f = open(filename, 'r');
    for line in f:
        genre, ident = line.split('|')
        batch.get_or_create_in_index(neo4j.Node, 'Genre', 'genre_id', ident, node({'genre_id': int(ident), 'name': genre}))
        
    
    nodes = batch.submit()
    batch.clear()
    
    print nodes
    
    print "ENDED"
    
    f.close()
    
    return nodes



if __name__ == "__main__":
    createNodesGenre('ml-100k/u.genre')