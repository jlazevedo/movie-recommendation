from py2neo import neo4j, node, rel
import time
start_time = time.time()

graph_db = neo4j.GraphDatabaseService()

batch = neo4j.WriteBatch(graph_db)

if __name__ == "__main__":

    OLE = 0
    sum_mae = 0
    sum_mae_float = 0

    f = open('ml-100k/u1.test', 'r');
    for i, line in enumerate(f):
        print i, ":",
        person_id, movie_id, rate, timestamp = line.split('\t')

        # query that considers Occupation and Age (returns null almost always)

        query = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), "
                "b=node:Movie(movie_id='"+movie_id+"') match p=a-[q:Works_In]->w<-[e:Works_In]-d-[t:Rates]->b "
                "where a.age + 10 > d.age and a.age - 10 < d.age return avg(t.rating)")

        # should be used when we assume that exists a certain generation that loves this movie. Nostalgic Relation

        query2 = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), "
                "b=node:Movie(movie_id='"+movie_id+"') match d-[t:Rates]->b"
                "where a.age + 10 > d.age and a.age - 10 < d.age return avg(t.rating)")

