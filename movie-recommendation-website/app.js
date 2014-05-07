/**
 * EADW
 *
 * app.js
 * 
 */

var connect = require('connect');
var express = require('express');
var exphbs = require('express3-handlebars');
var routes = {
    rate_movie: require('./routes/rate_movie'),
    after_rate_movie: require('./routes/after_rate_movie'),
    get_recommendation: require('./routes/get_recommendation')
}

var port = process.env.ACAD_API_PORT || 3000;


var app = exports.app = express();

app.use(connect.responseTime());
app.use(express.logger());
app.use(express.compress());
app.use(express.json());
app.use(express.urlencoded());
app.use(app.router);

app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');
app.set('views', __dirname + '/views');

if ('development' == app.get('env')) {
    app.use(express.errorHandler());
};


// API routes

app.get('/rate-movie', routes.rate_movie);
app.post('/rate-movie', routes.after_rate_movie);
app.get('/get-recommendation', routes.get_recommendation);


// server control

exports.server = app.listen(port, function () {
    console.log('Server listening on port', port);
});