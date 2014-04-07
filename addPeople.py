from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService()
graph_db.clear()

batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

# create a single node
def createNodesfromUserFile(filename):
    f = open(filename, 'r');
    for line in f:
        ident, age, gender, occupation, postal = line.split('|')
        people = batch.get_or_create_in_index(neo4j.Node, 'People', 'people_id', ident, node({'people_id': ident, 'age': age}))
        occup = batch.get_or_create_in_index(neo4j.Node, 'Occupation', 'occupation_id', occupation, node({'occupation_id': occupation}))
        relationship = batch.get_or_create_in_index(neo4j.Relationship, 'Works_In', 'works_in_id', occupation+postal, rel(people, 'Works_In', occup))
        
    
    nodes = batch.submit()
    batch.clear()
    
    print "ENDED"
    
    f.close()
    
    return nodes
    
def labelNodes(filename, nodes):
    f = open(filename, 'r');
    
    for i, line in enumerate(f):
        ident, age, gender, occupation, postal = line.split('|')        
        batch.add_labels(nodes[i * 3], 'MALE' if gender == 'M' else 'FEMALE' )
    
    batch.submit()
    
    print "ENDED"
    
    f.close()

    
if __name__ == "__main__":
    labelNodes('ml-100k/u.user', createNodesfromUserFile('ml-100k/u.user'))
    