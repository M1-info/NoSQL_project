import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt

mongo = Mongo()

film = 'Demain révolution'

pipeline = [
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$match': {'films.title': film}},
    {'$group': {
        '_id': '$name', 
        'total_price': {'$push': '$films.filmShow.price'},
        'recipe': {'$first': '$films.recipe'},
        'numberEntries': {'$first': '$films.numberEntries'},
        'numberSessions': {'$sum': 1}
        }
    },
    {'$project': {
        '_id': 0,
        'name': '$_id',
        'recipe': 1,
        'numberEntries': 1,
        'average_price': {'$round': [{'$avg': '$total_price'}, 2]},
        'numberSessions': 1
        }
    }
]

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)

print("Résultats pour le film \"" + film + "\" :\n")
for doc in data:
    print("Cinema \"" + doc['name'] + "\" :")
    print("     Nombre de séances : " + str(doc['numberSessions']))
    print("     Prix moyen séance: " + str(doc['average_price']) + "€")
    print("     Recette : " + str(doc['recipe']) + "€")
    print("     Nombre d'entrées : " + str(doc['numberEntries']))
    print("")

# plot the results in histogram
fig, ax = plt.subplots()

y = [doc["recipe"] for doc in data]
x = [doc["name"] for doc in data]

ax.bar(x, y, color='green', width=0.5)

ax.set_xlabel('Cinéma')
ax.set_ylabel('Recette (€)')

ax.set_title('Recette du film "' + film + '" par cinéma')

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()
