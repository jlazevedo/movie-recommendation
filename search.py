import imdb
movie = "Spiderman"
ia = imdb.IMDb()
results = ia.search_movie('Spiderman')
print results
mv = results[0] #First result

URL = ia.get_imdbURL(mv) #URL for first result
print URL
