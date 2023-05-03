import sys
sys.path.append('../utils')

from MongoDB import Mongo
from datetime import datetime

mongo = Mongo()

start_date = datetime(2018, 1, 1)
end_date = datetime(2020, 12, 31)

pipeline = [
    {'$match': {'$and': [{'releaseDate': {'$gte': start_date}}, {'releaseDate': {'$lte': end_date}}]}},
    {'$unwind': '$categories'},
    {'$group': {
        '_id': {
            'year': {'$year': '$releaseDate'},
            'categories': '$categories'
        },
        'recipe': {'$sum': '$recipe'},
        'numberEntries': {'$sum': '$numberEntries'}
    }},
    {'$project': {
        '_id': 1,
        'recipe': 1,
        'numberEntries': 1,
    }},
    {'$sort': {'_id.year': -1, 'recipe': -1}},
]

result = mongo.db.films.aggregate(pipeline)

current_year = None
print("L'évolution de la recette par catégorie des films sortis entre "+ start_date.strftime("%Y") +" au "+ end_date.strftime("%Y") +" est : \n")
for doc in result:
    if current_year != doc['_id']['year']:
        current_year = doc['_id']['year']
        print("Année : " + str(doc['_id']['year']))
    print("     Catégorie : " + doc['_id']['categories'])
    print("     Recette totale : " + str(doc['recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['numberEntries']))
    print("")

    

