from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)
    
if __name__ == "__main__":
    
    OLE = 0
    
    f = open('ml-100k/u1.test', 'r');
    for i, line in enumerate(f):
        print i, ":",
        person_id, movie_id, rate, timestamp = line.split('\t')
    
        query = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), b=node:Movie(movie_id='"+movie_id+"') match p=a-[r:Rates]->c<-[s:Rates]-d-[t:Rates]->b,c-[u:Genre_As]->g<-[v:Genre_As]-b where r.rating = s.rating return p")
    
        person = batch.get_or_create_in_index(neo4j.Node, 'People', 'people_id', person_id, node())
        movie = batch.get_or_create_in_index(neo4j.Node, 'Movie', 'movie_id', movie_id, node())
        
        relationship = batch.get_or_create_in_index(neo4j.Relationship, 'Rates', 'rate_id', person_id+':'+movie_id, rel(person, ('Rates',{'rating':int(rate)}), movie))
        
        batch.submit()
        batch.clear()
        
        #print query
    
        i = 0.0
        value = 0
    
        for record in query.stream():
        
            r = record.values[0].relationships
            r1, r2, r3 = record.values[0].relationships
            #print r1.get_properties()['rating'], r2.get_properties()['rating'], r3.get_properties()['rating']
            value += r3.get_properties()['rating']
            i += 1.0
        
        if (round(i) == 0):
            i = 1;
            
        print value/i, rate,
        
        if (round(value/i) == float(rate)):
            print "\t[X]"
            OLE += 1
        else:
            print "\t[ ]"
    
    f.close()
    
    print OLE