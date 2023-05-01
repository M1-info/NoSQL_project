import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()


pipeline = [
    {'$unwind': '$actors'},
    {'$group': {
        '_id': '$actors',
        'total_recipe': {'$sum': '$recipe'},
        'total_number_entries': {'$sum': '$numberEntries'},
        'number_of_films': {'$sum': 1}
    }},
    {'$project': {
        '_id': 0,
        'actor': '$_id',
        'total_recipe': 1,
        'total_number_entries': 1,
        'number_of_films': 1
    }},
    {'$sort': {'total_recipe': -1}},
    {'$limit': 5}
]

result = mongo.db.films.aggregate(pipeline)

print("Les acteurs les plus rentables sont : \n")
for doc in result:
    print("Acteur : " + doc['actor']['firstName'] + " " + doc['actor']['lastName'])
    print("     Recette totale : " + str(doc['total_recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['total_number_entries']))
    print("     Nombre de films : " + str(doc['number_of_films']))
    print("")