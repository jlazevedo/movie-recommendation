from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)
    
if __name__ == "__main__":
    
    OLE = 0
    
    f = open('ml-100k/u1.test', 'r');
    for i, line in enumerate(f):
        print i, ":",
        person_id, movie_id, rate, timestamp = line.split('\t')
    
        query = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), "
                "b=node:Movie(movie_id='"+movie_id+"') match p=a-[r:Rates]->c<-[s:Rates]-d-[t:Rates]->b, "
                        "c-[u:Genre_As]->g<-[v:Genre_As]-b where r.rating = s.rating return avg(t.rating)")
    
        person = batch.get_or_create_in_index(neo4j.Node, 'People', 'people_id', person_id, node())
        movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', movie_id, node())
        
        relationship = batch.get_or_create_in_index(neo4j.Relationship, 'Rates', 'rate_id',
                                            person_id+':'+movie_id, rel(person, ('Rates',{'rating':int(rate)}), movie))
        
        batch.submit()
        batch.clear()

        result = 0
    
        for record in query.stream():

            if record.values[0] is None:
                result = 0
            else:
                result = float(record.values[0])

        print result, rate,
        
        if (round(result) == float(rate)):
            print "\t[X]"
            OLE += 1
        else:
            print "\t[ ]"

        if (i % 1000 == 0):
            print 'OK: ' + str(OLE)
    
    f.close()
    
    print OLE