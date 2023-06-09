import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt

mongo = Mongo()


film_title = 'Demain révolution'

pipeline = [
    {'$unwind': '$films'},
    {'$match': {'films.title': film_title}},
    {'$unwind': '$films.filmShow'},
    {'$group': {
        '_id': {'$hour': '$films.filmShow.startShow'},
        'recipe': {'$sum': '$films.filmShow.recipe'},
        'numberEntries': {'$sum': '$films.filmShow.numberEntries'},
        'enterPerShow': {'$avg': '$films.filmShow.numberEntries'},
        'numberShows': {'$sum': 1}
    }},
    {'$project': {
        '_id': 1,
        'recipe': 1,
        'numberEntries': 1,
        'enterPerShow': {'$round' : ['$enterPerShow', 0]},
        'numberShows': 1
    }},
    {'$sort': {'_id': -1}}
]

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)

print("Statistique des heures de projection les plus rentables pour le film \""+ film_title + "\" :")
for doc in data:
    print("Heure : {}h".format(doc['_id']))
    print("     Recette : {}€".format(doc['recipe']))
    print("     Nombre d'entrées : {}".format(doc['numberEntries']))
    print("     Nombre de séances : {}".format(doc['numberShows']))
    print("     Nombre moyen d'entrées par séance : {}".format(doc['enterPerShow']))
    print()

# plot the results in histogram
fig, ax = plt.subplots()

y = [doc["recipe"] for doc in data]
x = [doc["_id"] for doc in data]

ax.bar(x, y, color='green', width=0.5)

ax.set_xlabel('Heure')
ax.set_ylabel('Recette (€)')

ax.set_title('Recette du film "' + film_title + '" par heure de projection')

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()