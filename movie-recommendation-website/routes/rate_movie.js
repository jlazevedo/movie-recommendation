

var neo4j = require('neo4j');
var db = new neo4j.GraphDatabase('http://localhost:7474');

module.exports = function(req, res) {

    num = Math.floor((Math.random() * 1682) + 1);
    
    db.getIndexedNode('Movie', 'movie_id', num+'', function(err, node){
 
        res.render('rate_movie', {  'img': node._data.data.img,
                                    'title': node._data.data.title,
                                    'movie_id': node._data.data.movie_id,
                                    'id': req.query.id
                                 });  
    
    });
    
    
}