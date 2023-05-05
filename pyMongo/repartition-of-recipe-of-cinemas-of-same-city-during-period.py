import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt
from datetime import datetime

mongo = Mongo()

### Filters ###
city = 'Dijon'

# Period :
start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 1, 1)


pipeline = [
    {'$match': {'city': city}},
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$match': {
        'films.filmShow.dateShow': {
            '$gte': start_date,
            '$lte': end_date
            }
        }
    },
    {'$group': {
        '_id': '$films.title',
        'recipe_film': {'$sum': "$films.filmShow.recipe"},
        'cinema_name': {'$first': '$name'}
        }
    },
    {'$facet': {
        'total_recipe': [{
            '$group': {
                '_id': 'null',
                'total_recipe': {'$sum': '$recipe_film'}
            }
        }],
        'groupFilms': [{
            '$group': {
                '_id': '$cinema_name',
                'total_recipe_cinema': {'$sum': '$recipe_film'}
            }
        }]}
    },
    { '$addFields': {
        'total_recipe': {
            '$arrayElemAt': ['$total_recipe', 0 ]
            }
        }
    },
    {
        '$unwind': '$groupFilms'
    },
    { '$project': {
        '_id': 0,
        'cinema_name': '$groupFilms._id',
        'recipe_cinema': '$groupFilms.total_recipe_cinema',
        'pourcentage': {
            '$multiply': [
                {
                    '$divide': [
                        '$groupFilms.total_recipe_cinema',
                        '$total_recipe.total_recipe'
                    ]
                },
                100
            ]
        }
    } },
]

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)

print("Voici la répartition des recettes liées au cinéma pour la ville de " + city + " sur la période " + start_date.strftime("%d-%m-%Y") + " - " + end_date.strftime("%d-%m-%Y") + " :\n")
for doc in data:
    print("Cinéma : " + doc['cinema_name'] + " \t| Recette : " + str(doc['recipe_cinema']) + " \t| Pourcentage : " + str(round(doc['pourcentage'], 2)) + "%")


# plot the results in histogram

fig, ax = plt.subplots()

y = [doc["pourcentage"] for doc in data]
x = [doc["cinema_name"] for doc in data]

ax.pie(y, labels=x, autopct='%1.1f%%', startangle=90)

ax.set_title('Répartition des recettes liées au cinéma pour la ville de ' + city + ' sur la période ' + start_date.strftime("%d-%m-%Y") + ' - ' + end_date.strftime("%d-%m-%Y"))

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()
