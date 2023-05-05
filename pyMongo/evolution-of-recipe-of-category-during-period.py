import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt
from datetime import datetime

mongo = Mongo()

category = "Animation"
start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 12, 31)

pipeline = [
    {'$match': {
        '$and': [
            {'releaseDate': {'$gte': start_date}}, 
            {'releaseDate': {'$lte': end_date}},
            {'categories': category}
        ]
    }},
    {'$group': {
        '_id': {'$year': '$releaseDate'},
        'recipe': {'$sum': '$recipe'},
        'numberEntries': {'$sum': '$numberEntries'}
    }},
    {'$project': {
        '_id': 1,
        'recipe': 1,
        'numberEntries': 1,
    }},
    {'$sort': {'_id': -1}},
]

result = mongo.db.films.aggregate(pipeline)
data = list(result)

current_year = None
print("L'évolution des recettes des films de catégorie "+ category +" sortis entre "+ start_date.strftime("%Y") +" au "+ end_date.strftime("%Y") +" est : \n")
for doc in data:
    if current_year != doc['_id']:
        current_year = doc['_id']
        print("Année : " + str(doc['_id']))
    print("     Recette totale : " + str(doc['recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['numberEntries']))
    print("")

# plot the results in histogram
fig, ax = plt.subplots()

y = [doc["recipe"] for doc in data]
x = [doc["_id"] for doc in data]

ax.plot(x, y, color='green')

ax.set_xlabel('Année')
ax.set_ylabel('Recette (€)')

ax.set_title("L'évolution des recettes des films de catégorie "+ category +" sortis entre "+ start_date.strftime("%Y") +" au "+ end_date.strftime("%Y"))

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()