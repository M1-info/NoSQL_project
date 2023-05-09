import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt

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

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)[0]

print("Voici les catégories de films les plus rentables du cinéma \"" + cinema + "\" sachant que :")
print("Nombre total de films : " + str(data['total_nbFilms']))
print("Nombre total d'entrées : " + str(data['total_numberEntries']))
print("Recette totale : " + str(data['total_recipe']) + "\n")
for doc in data['categories']:
    print('Catégorie : ' + doc['category'])
    print('     Nombre de films : ' + str(doc['nbFilms']))
    print('     Nombre d\'entrées : ' + str(doc['numberEntries']))
    print('     Recette : ' + str(doc['recipe']))
    print('     Pourcentage de films : ' + str(doc['percent_nbFilms']))
    print('     Pourcentage d\'entrées : ' + str(doc['percent_numberEntries']))
    print('     Pourcentage de recette : ' + str(doc['percent_recipe']))
    print('')


# plot the results
labels = []
sizes = []
for doc in data['categories']:
    labels.append(doc['category'])
    sizes.append(doc['percent_recipe'])

fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
ax1.axis('equal')

# make the plot full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

# show the plot
plt.title('Recette par catégorie de film du cinéma "' + cinema + '"', loc='center', pad=30)
plt.legend(loc = 'upper right', labels=['%s, %1.1f %%' % (l, s) for l, s in zip(labels, sizes)])
plt.show()

mongo.close()