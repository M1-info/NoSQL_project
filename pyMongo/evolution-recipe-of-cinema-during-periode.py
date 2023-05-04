import sys
sys.path.append('../utils')

from MongoDB import Mongo
from pprint import pprint
from datetime import datetime

mongo = Mongo()

cinema = 'Charpentier et Fils'
start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 12, 31)

pipeline = [
    {'$match': {'name': cinema}},
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$match': {
        '$and': [
            {'films.filmShow.dateShow': {'$gte': start_date}},
            {'films.filmShow.dateShow': {'$lte': end_date}}
        ]
    }},
    {'$group': {
        '_id': {'$year': '$films.filmShow.dateShow'},
        'recipe': {'$sum': '$films.filmShow.recipe'}
    }},
    {'$sort': {'_id': 1}},
    {'$project': {
        '_id': 0,
        'year': '$_id',
        'recipe': 1
        }
    }
]

result = mongo.db.cinemas.aggregate(pipeline)

print("Evolution de la recette du cinéma " + cinema + " entre " + start_date.strftime("%Y") + " et " + end_date.strftime("%Y")+ " : \n")
for doc in result:
    print("     Année : " + str(doc['year']) + " | Recette : " + str(doc['recipe']) + "€")

mongo.close()