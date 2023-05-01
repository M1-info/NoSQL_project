import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

pipeline = [
    {'$unwind': '$films'},
    {'$group': {
        '_id': '$name',
        'number_films': {'$sum': 1},
        'total_recipe': {'$sum': '$films.recipe'},
        'total_number_entries': {'$sum': '$films.numberEntries'},
        'average_recipe': {'$avg': '$films.recipe'},
    }},
    {'$project': {
        '_id': 0,
        'name': '$_id',
        'number_films': 1,
        'total_recipe': 1,
        'total_number_entries': 1,
        'average_recipe': {'$round': ['$average_recipe', 2]}
        }
    },
    {'$sort': {'total_recipe': -1, 'total_number_entries': -1, 'number_films': -1}},
    {'$limit': 3},
]

result = mongo.db.categories.aggregate(pipeline)

print("Les categories les plus rentables sont :\n")
for doc in result:
    print("Categorie \"" + doc['name'] + "\" :")
    print("     Nombre de films : " + str(doc['number_films']))
    print("     Recette totale : " + str(doc['total_recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['total_number_entries']))
    print("     Recette moyenne par film : " + str(doc['average_recipe']) + "€")
    print("")

mongo.close()
