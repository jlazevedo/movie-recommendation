import requests
from rottentomatoes import RT


r = requests.get("http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)")

print r.url


print RT('6psypq3q5u3wf9f2be38t5fd').search('Toy Story (1995)')


import imdb

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb() # by default access the web.

m = ia.get_movie('0114709')

print m['director']