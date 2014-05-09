from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

# create a single node
def createVotesfromFile(filename):
    f = open(filename, 'r');
    for i, line in enumerate(f):
        print i
        person_id, movie_id, rate, timestamp = line.split('\t')
        
        person = batch.get_or_create_in_index(neo4j.Node, 'People', 'people_id', person_id, node())
        movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', movie_id, node())
        
        relationship = batch.get_or_create_in_index(neo4j.Relationship, 'Rates', 'rate_id', person_id+':'+movie_id, rel(person, ('Rates',{'rating':int(rate)}), movie))
        
        if i % 1000 == 0:
            nodes = batch.submit()
            batch.clear()
            
    nodes = batch.submit()
    batch.clear()
    
    print "ENDED"
    
    f.close()
    
    return nodes
    
if __name__ == "__main__":
   createVotesfromFile('ml-100k/u1.base')