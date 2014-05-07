

var neo4j = require('neo4j');
var db = new neo4j.GraphDatabase('http://localhost:7474');
var _ = require('underscore');

module.exports = function(req, res) {

    array = [];
    
    db.query("start a=node:People(people_id='"+req.query.id+"') match p=a-[r:Rates]->c-[s:Genre_As]->g<-[v:Genre_As]-d<-[q:Rates]-() where r.rating = 5 and q.rating = 5 with d,g,a, sum(q.rating) as total, count(q) as counter order by total desc match d where not a-[:Rates]->d return distinct(d) limit 10", function (err, nodes) {
    
        console.log(nodes);
        
    _.each(nodes, function(node) {
    
        array.push(node.d._data.data);
    
    });
        
        res.render('get_recommendations',{'movies': array});
    
    
    });
    
    
}