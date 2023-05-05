import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt
from datetime import datetime

mongo = Mongo()

start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 12, 31)

pipeline = [
    {'$match': {'$and': [{'releaseDate': {'$gte': start_date}}, {'releaseDate': {'$lte': end_date}}]}},
    {'$unwind': '$categories'},
    {'$group': {
        '_id': {
            'year': {'$year': '$releaseDate'},
            'categories': '$categories'
        },
        'recipe': {'$sum': '$recipe'},
        'numberEntries': {'$sum': '$numberEntries'}
    }},
    {'$project': {
        '_id': 1,
        'recipe': 1,
        'numberEntries': 1,
    }},
    {'$sort': {'_id.year': -1, 'recipe': -1}},
]

result = mongo.db.films.aggregate(pipeline)
data = list(result)

current_year = None
print("L'évolution de la recette par catégorie des films sortis entre "+ start_date.strftime("%Y") +" au "+ end_date.strftime("%Y") +" est : \n")
for doc in data:
    if current_year != doc['_id']['year']:
        current_year = doc['_id']['year']
        print("Année : " + str(doc['_id']['year']))
    print("     Catégorie : " + doc['_id']['categories'])
    print("     Recette totale : " + str(doc['recipe']) + "€")
    print("     Nombre d'entrées total : " + str(doc['numberEntries']))
    print("")

# plot the results in histogram
# create a line for each category

fig, ax = plt.subplots()

categories = []
for doc in data:
    if doc['_id']['categories'] not in categories:
        categories.append(doc['_id']['categories'])

for category in categories:
    y = [doc["recipe"] for doc in data if doc['_id']['categories'] == category]
    x = [doc["_id"]["year"] for doc in data if doc['_id']['categories'] == category]

    ax.plot(x, y, label=category)

ax.set_xlabel('Année')
ax.set_ylabel('Recette (€)')

ax.set_title("L'évolution de la recette par catégorie des films sortis entre "+ start_date.strftime("%Y") +" au "+ end_date.strftime("%Y"),
             pad=40)

ax.legend(loc='upper left', bbox_to_anchor=(0.1, 1.05),
          ncol=3, fancybox=True, shadow=True)

# maximize the window
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()