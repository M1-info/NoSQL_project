import sys
sys.path.append('..')

from MongoDB import Mongo
import json
import os
import datetime

mongo = Mongo()
db = mongo.db

path = os.path.join(os.path.dirname(__file__), '../../data/')

# load data from json files
films = json.load(open(path + 'films.json', 'r', encoding='utf8'))
categories = json.load(open(path + 'categories.json', 'r', encoding='utf8'))
cinemas = json.load(open(path + 'cinemas.json', 'r', encoding='utf8'))

# load schemas from json files
films_schema = json.load(open(path + 'schemas/collection_film.json', 'r', encoding='utf8'))
categories_schema = json.load(open(path + 'schemas/collection_categorie.json', 'r', encoding='utf8'))
cinemas_schema = json.load(open(path + 'schemas/collection_cinema.json', 'r', encoding='utf8'))

# convert date string to datetime
for film in films:
    film["releaseDate"] = datetime.datetime.strptime(film["releaseDate"], "%Y-%m-%d")

for cinema in cinemas:
    for film in cinema["films"]:
        film["startDiffusion"] = datetime.datetime.strptime(film["startDiffusion"], "%Y-%m-%d")
        film["endDiffusion"] = datetime.datetime.strptime(film["endDiffusion"], "%Y-%m-%d")
        for show in film["filmShow"]:
            show["dateShow"] = datetime.datetime.strptime(show["dateShow"], "%Y-%m-%d")
            show["startShow"] = datetime.datetime.strptime(show["startShow"], "%Y-%m-%dT%H:%M:%S")
            show["endShow"] = datetime.datetime.strptime(show["endShow"], "%Y-%m-%dT%H:%M:%S")


# drop collections if already exist
db.drop_collection('films')
db.drop_collection('categories')
db.drop_collection('cinemas')

# create collections with schemas validation
db.create_collection('films', validator={"$jsonSchema":films_schema})
db.create_collection('categories', validator={"$jsonSchema":categories_schema})
db.create_collection('cinemas', validator={"$jsonSchema":cinemas_schema})

# create indexes to have unique values for titles in films, name in categories and cinemas
db.films.create_index([('title', 1)], unique=True)
db.categories.create_index([('name', 1)], unique=True)
db.cinemas.create_index([('name', 1)], unique=True)

# insert data in collections
db.films.insert_many(films)
db.categories.insert_many(categories)
db.cinemas.insert_many(cinemas)

