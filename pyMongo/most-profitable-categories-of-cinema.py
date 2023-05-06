import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

filter = {
    'name': 'Charpentier et Fils'
}

pipeline = [
    {'$match': filter},
    {'$unwind': '$films'},
    # lookup the film collection
    {'$lookup': {
        'from': 'films',
        'localField': 'films.film',
        'foreignField': '_id',
        'as': 'film'
    }},
    # lookup returns an array, so we need to get the first element
    # because we know that there is only one element
    {'$project': {
        'film': {'$arrayElemAt': ['$film', 0]},
        'films.recipe': 1,
        'films.numberEntries': 1
    }},
    # unwind the categories array
    {'$unwind': '$film.categories'},
    # group by category and sum the recipe and number of entries
    {'$group': {
        '_id': '$film.categories',
        'total_recipe': {'$sum': '$films.recipe'},
        'total_number_entries': {'$sum': '$films.numberEntries'},
        'number_of_films': {'$sum': 1}
    }},
    {'$project': {
        '_id': 0,
        'category': '$_id',
        'total_recipe': 1,
        'total_number_entries': 1,
        'number_of_films': 1
    }},
    {'$sort': {'total_recipe': -1}},
    {'$limit': 5}
]

result = mongo.db.cinemas.aggregate(pipeline)

print("Les catégories de films les plus rentables du cinéma \"" + filter['name'] + "\" sont : \n")
for doc in result:
    print("Categorie : " + doc['category'])
    print("     Nombre de films : " + str(doc['number_of_films']))
    print("     Recette totale : " + str(doc['total_recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['total_number_entries']))
    print("")

mongo.close()