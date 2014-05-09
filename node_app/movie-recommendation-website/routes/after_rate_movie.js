

var neo4j = require('neo4j');
var db = new neo4j.GraphDatabase('http://localhost:7474');

module.exports = function(req, res) {

    db.getIndexedNode('People', 'people_id', req.body.user_id, function(err, node) {
        
        db.getIndexedNode('Movie', 'movie_id', req.body.movie_id, function(err, movie) {
                       
           node.createRelationshipTo(movie, 'Rates', {'rating':parseInt(req.body.rate)},
                                     function(err, val) {
                                     
                                     
                                        console.log(val);
                                     
                                     
                                     });  
                       
        });
    });
    
    res.redirect('/rate-movie?id=' + req.body.user_id);
    
}