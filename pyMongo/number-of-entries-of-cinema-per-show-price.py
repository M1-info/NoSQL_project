import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt

mongo = Mongo()

cinema = 'Charpentier et Fils'

pipeline = [
    {'$match': {'name': cinema}},
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$group': {
        '_id': '$films.filmShow.price',
        'number_of_entries': {'$sum': '$films.filmShow.numberEntries'},
        'number-of_shows': {'$sum': 1},
        'average_number_of_entries': {'$avg': '$films.filmShow.numberEntries'}
    }},
    {'$project': {
        '_id': 0,
        'price': '$_id',
        'number_of_entries': 1,
        'number-of_shows': 1,
        'average_number_of_entries': {
            '$trunc': [{'$round': ['$average_number_of_entries', 0]}, 0]
        }
    }},
    {'$sort': {'price': 1}}
]

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)

current_price = 0
print("Nombre d'entrées par prix de place dans le cinéma \"" + cinema + "\" : \n")
for doc in data:
    if doc['price'] != current_price:
        print("Prix de place : " + str(doc['price']) + "€")
        current_price = doc['price']
    print("     Nombre d'entrées : " + str(doc['number_of_entries']))
    print("     Nombre de séances : " + str(doc['number-of_shows']))
    print("     Nombre moyen d'entrées par séance : " + str(doc['average_number_of_entries']))
    print("")

# plot the results in histogram
fig, ax = plt.subplots()

y = [doc["average_number_of_entries"] for doc in data]
x = [doc["price"] for doc in data]

ax.bar(x, y, color='green', width=0.5)

ax.set_xlabel('Prix de place (€)')
ax.set_ylabel('Nombre moyen d\'entrées par séance')
ax.set_title('Nombre moyen d\'entrées par prix de place dans le cinéma "' + cinema + '"')

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()