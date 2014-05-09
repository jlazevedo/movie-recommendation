

var neo4j = require('neo4j');
var db = new neo4j.GraphDatabase('http://localhost:7474');
var _ = require('underscore');

module.exports = function(req, res) {

    array = [];
    
    array2 = [];
    
    db.query("start a=node:People(people_id='"+req.query.id+"') match p=a-[r:Rates]->c-[s:Genre_As]->g<-[v:Genre_As]-d<-[q:Rates]-() where r.rating = 5 and q.rating = 5 with d,g,a, sum(q.rating) as total, count(q) as counter order by total desc match d where not a-[:Rates]->d return distinct(d) limit 100", function (err, nodes) {
    
        console.log(nodes);
        
    _.each(nodes, function(node) {
        
        db.query("start a=node:Movie(movie_id='"+node.d._data.data.movie_id+"') return labels(a)", function (err, labels) {
        
        
        console.log(labels[0]['labels(a)']);
        
        
            if (labels[0]['labels(a)'] != [])
                if (array2 == []) {
                    array2 = labels[0]['labels(a)'];
                    array.push(node.d._data.data);
                } else
                    if (_.intersection(array2,labels[0]['labels(a)']) != []) {
                        array2 = array2.concat(labels[0]['labels(a)']);
                        array.push(node.d._data.data);
                }
            
        
            if (nodes[nodes.length -1] == node)
                res.render('get_recommendations',{'movies': array});
            
        });
        
    });
        
    });
    
    
}