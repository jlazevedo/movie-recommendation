import requests
import simplejson
import nltk
from nltk.corpus import movie_reviews
from bs4 import BeautifulSoup
from nltk.corpus import stopwords





def getReviewsAdjectivesByIMDB(filename,output):






    stop = stopwords.words('english')

    f = open(filename, 'r')
    file = open(output, 'w+')
    words = open('words.txt','r')
    good_words = []

    for line in words:
        line = line.replace('\n','')
        good_words.append(line)


    for z,line in enumerate(f):
        adjectives=[]

        values = line.split('|')

        ident = values[0]
        if ident in [str(267),str(1358),str(1359)]:
            continue
        title = values[1]
        imdb = values[3]
        genre = values[4:]
        movie_genres = []


        print (title)
        print z+1
        print imdb

        request = requests.get("http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json?apikey=rh8chjzp8vu6gnpwj88736uv&type=imdb&id=" + imdb)

        data = request.content


        js = simplejson.loads(data)

        try:

            links = js["links"]
            reviews = links["reviews"]
            reviews = reviews + "?apikey=rh8chjzp8vu6gnpwj88736uv"

            reviewsRequest = requests.get(reviews)
            reviews_data = reviewsRequest.content
            reviews_js = simplejson.loads(reviews_data)

        except KeyError,e:
            continue

        article = None


        for i,review in enumerate(reviews_js['reviews']):

            try:
                if "http://movies.nytimes.com" in review["links"]["review"]:
                    reviewURL = review["links"]["review"]
                    review_html = requests.get(reviewURL)
                    soup = BeautifulSoup(review_html.content)
                    article = soup.find(id="articleBody")
                    tokens = nltk.word_tokenize(str(article))
                    tagged = nltk.pos_tag(tokens)
                    for word, tag in tagged:

                        if tag in ['NN'] and len(adjectives)<10 and word in good_words and word not in adjectives and word not in ['movie','screen','genre','start','end','make','film','director','trailer','(',')','cast','actor','tone'] and word not in stop:
                            try:
                                word = word.encode('ascii','ignore')
                                adjectives.append(word)
                            except UnicodeDecodeError,e:
                                continue
                    break
            except KeyError,e:
                continue


        print (adjectives)
        print >>file, adjectives









if __name__ == "__main__":
    getReviewsAdjectivesByIMDB("finalfile2.txt", "adjectives.txt")