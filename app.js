
/**
 * Module dependencies.
 */

 var express = require('express'),
 routes = require('./routes'),
 http = require('http'),
 path = require('path'),
 db = require('mongoskin').db('mongodb://localhost:27017/dvds'),
 movies = db.collection('movies');

 var app = express();

 app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.favicon(__dirname + '/public/images/favicon.ico', { maxAge: 2592000000 }));
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(require('stylus').middleware(__dirname + '/public'));
  app.use(express.directory(path.join(__dirname, 'public')));
  app.use(express.static(path.join(__dirname, 'public')));

});

 app.configure('development', function(){
  app.use(express.errorHandler());
});

 app.get('/', function(req,res){
  res.render('movies', {title: "DVD Ninja"});
});


 app.get('/dvds', function(req,res){
  console.log('hey')
  var query = req.query;
  var start_date = new Date(query.start_date);
  var end_date = new Date(query.end_date);
  var genr = ".*" + query.genre + ".*";
  var critic_rating = parseInt(query.critic_rating);
  var audience_rating = parseInt(query.audience_rating);
  var movie_query = '.*' + req.param('movie_query') + '.*';
  console.log(movie_query);
  console.log(typeof critic_rating)
  res.writeHead(200, {'Access-Control-Allow-Origin': '*'/*, "Content-Type": "application/json"*/});
  movies.find({dvd_release_date: {$gte: start_date, $lte: end_date}, genre: {
    $regex: genr}, title: {$regex: movie_query, $options: 'i'}, critic_rating:{$gte: critic_rating, $nin:['No Reviews Yet...', 'No Score Yet...']}, audience_rating:{$gte:audience_rating, $nin:['No Reviews Yet...', 'No Score Yet...']}}, {
      title:1, dvd_release_date:1, critic_rating:1, audience_rating:1, torrents:1, actors:1, _id:0}).sort(
      {dvd_release_date:-1}).limit(100).toArray(function (e, result){
        if (e) throw(e);
        res.end(JSON.stringify(result));
      });
  });

 http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});

app.get('/restaurants', function(req, res){
  console.log('Enter Restaurant Week');
  res.end("You want a menu, don't you?");
});
