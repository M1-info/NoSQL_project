import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

cinema = 'Charpentier et Fils'

pipeline = [
    {'$match': {'name': cinema}},
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$group': {
        '_id': '$films.filmShow.price',
        'number_of_entries': {'$sum': '$films.filmShow.numberEntries'},
        'number-of_shows': {'$sum': 1},
        'average_number_of_entries': {'$avg': '$films.filmShow.numberEntries'}
    }},
    {'$project': {
        '_id': 0,
        'price': '$_id',
        'number_of_entries': 1,
        'number-of_shows': 1,
        'average_number_of_entries': {
            '$trunc': [{'$round': ['$average_number_of_entries', 0]}, 0]
        }
    }},
    {'$sort': {'price': 1}}
]

result = mongo.db.cinemas.aggregate(pipeline)

current_price = 0
print("Nombre d'entrées par prix de place dans le cinéma \"" + cinema + "\" : \n")
for doc in result:
    if doc['price'] != current_price:
        print("Prix de place : " + str(doc['price']) + "€")
        current_price = doc['price']
    print("     Nombre d'entrées : " + str(doc['number_of_entries']))
    print("     Nombre de séances : " + str(doc['number-of_shows']))
    print("     Nombre moyen d'entrées par séance : " + str(doc['average_number_of_entries']))
    print("")
