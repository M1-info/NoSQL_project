from pyMongo.utils.MongoDB import Mongo
import json
import os

mongo = Mongo()
db = mongo.db

path = os.path.join(os.path.dirname(__file__), '..')

films = json.load(open(path + 'films.json', 'r', encoding='utf8'))
# categories = json.load(open(path + 'categories.json', 'r', encoding='utf8'))
# cinemas = json.load(open(path + 'cinemas.json', 'r', encoding='utf8'))

films_schema = json.load(open(path + 'schemas/collection_film.json', 'r', encoding='utf8'))
# categories_schema = json.load(open(path + 'schemas/collection_categorie.json', 'r', encoding='utf8'))
# cinemas_schema = json.load(open(path + 'schemas/collection_cinema.json', 'r', encoding='utf8'))

print(db.create_collection('films', validator=films_schema))
# db.create_collection('categories', validator=categories_schema)
# db.create_collection('cinemas', validator=cinemas_schema)

# db.films.insert_many(films)
# db.categories.insert_many(categories)
# db.cinemas.insert_many(cinemas)

