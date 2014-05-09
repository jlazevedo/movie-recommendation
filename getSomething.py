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

        query = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), "
                "b=node:Movie(movie_id='"+movie_id+"') match p=a-[r:Rates]->c<-[s:Rates]-d-[t:Rates]->b, "
                "c-[u:Genre_As]->g<-[v:Genre_As]-b where r.rating = s.rating with a,d,t.rating as rate, "
                "count(distinct(c)) as total with a,d,rate,total order by total desc limit 10 "
                "with rate order by rate return avg(rate)")

        result = 0

        for record in query.stream():

            if record.values[0] is None:
                result = 0
            else:
                result = float(record.values[0])

        if result == 0:
            query2 = neo4j.CypherQuery(graph_db, "start a=node:People(people_id='" +person_id+"'), "
                "b=node:Movie(movie_id='"+movie_id+"') match p=a-[r:Rates]->c<-[s:Rates]-d-[t:Rates]->b "
                "where r.rating = s.rating with a,d,t.rating as rate, "
                "count(distinct(c)) as total with a,d,rate,total order by total desc limit 10 "
                "with rate order by rate return avg(rate)")

            result = 0

            for record in query2.stream():

                if record.values[0] is None:
                    result = 0
                else:
                    result = float(record.values[0])

            if result == 0:
                result = 3

        print result, rate,

        float_mae = abs(result - float(rate))
        mae = abs(round(result) - int(rate))

        print mae, float_mae,

        if (round(result) == float(rate)):
            print "\t[X]"
            OLE += 1
        else:
            print "\t[ ]"

        sum_mae += mae
        sum_mae_float += float_mae

        if (i % 100 == 0 and i != 0):
            print 'OK: ' + str(OLE), sum_mae/i, sum_mae_float/float(i)




    f.close()
    
    print 'OK: ' + str(OLE), sum_mae/i, sum_mae_float/float(i)


    print time.time() - start_time, "seconds"
