import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

cinema = 'Charpentier et Fils'

# get in percentage the recipe and number of entries per category
pipeline = [
    {'$match': {'name': cinema}},
    {'$unwind': '$films'},
    {'$lookup': {
        'from': 'films',
        'let': {'film_id': '$films.film'},
        'pipeline': [
            {'$match': {'$expr': {'$eq': ['$_id', '$$film_id']}}},
            {'$project': {'_id': 0, 'categories': 1}}
        ],
        'as': 'film'}
     },
    {'$project': {
        'film': {'$arrayElemAt': ['$film', 0]},
        'films.recipe': 1,
        'films.numberEntries': 1
    }},
    {'$unwind': '$film.categories'},
    {'$group': {
        '_id': '$film.categories',
        'recipe': {'$sum': '$films.recipe'},
        'numberEntries': {'$sum': '$films.numberEntries'},
        'nbFilms': {'$sum': 1},
    }},
    {'$group': {
        '_id': None,
        'total_nbFilms': {'$sum': '$nbFilms'},
        'total_recipe': {'$sum': '$recipe'},
        'total_numberEntries': {'$sum': '$numberEntries'},
        'categories': {'$push': {
            'category': '$_id',
            'nbFilms': '$nbFilms',
            'recipe': '$recipe',
            'numberEntries': '$numberEntries',
        }}
    }},
    {'$project': {
        '_id': 0,
        'total_nbFilms': 1,
        'total_recipe': 1,
        'total_numberEntries': 1,
        'categories': {
            '$map': {
                'input': '$categories',
                'as': 'category',
                'in': {
                    'category': '$$category.category',
                    'nbFilms': '$$category.nbFilms',
                    'recipe': '$$category.recipe',
                    'numberEntries': '$$category.numberEntries',
                    'percent_nbFilms': {
                        '$round':  [{'$multiply': [{'$divide': ['$$category.nbFilms', '$total_nbFilms']}, 100]}, 2]
                    },
                    'percent_recipe': {
                        '$round':  [{'$multiply': [{'$divide': ['$$category.recipe', '$total_recipe']}, 100]}, 2]
                    },
                    'percent_numberEntries': {
                        '$round':  [{'$multiply': [{'$divide': ['$$category.numberEntries', '$total_numberEntries']}, 100]}, 2]
                    },
                }
            }
        }
    }}
]

result = mongo.db.cinemas.aggregate(pipeline).next()

print("Les catégories de films les plus rentables du cinéma \"" + cinema + "\" sont : \n")
print("Nombre total de films : " + str(result['total_nbFilms']))
print("Nombre total d'entrées : " + str(result['total_numberEntries']))
print("Recette totale : " + str(result['total_recipe']))
for doc in result['categories']:
    print('Catégorie : ' + doc['category'])
    print('     Nombre de films : ' + str(doc['nbFilms']))
    print('     Nombre d\'entrées : ' + str(doc['numberEntries']))
    print('     Recette : ' + str(doc['recipe']))
    print('     Pourcentage de films : ' + str(doc['percent_nbFilms']))
    print('     Pourcentage d\'entrées : ' + str(doc['percent_numberEntries']))
    print('     Pourcentage de recette : ' + str(doc['percent_recipe']))
    print('\n')

mongo.close()