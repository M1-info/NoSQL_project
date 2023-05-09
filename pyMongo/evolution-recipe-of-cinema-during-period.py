import sys
sys.path.append('../utils')

from MongoDB import Mongo
from matplotlib import pyplot as plt
from datetime import datetime

mongo = Mongo()

cinema = 'Charpentier et Fils'
start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 12, 31)

pipeline = [
    {'$match': {'name': cinema}},
    {'$unwind': '$films'},
    {'$unwind': '$films.filmShow'},
    {'$match': {
        '$and': [
            {'films.filmShow.dateShow': {'$gte': start_date}},
            {'films.filmShow.dateShow': {'$lte': end_date}}
        ]
    }},
    {'$group': {
        '_id': {'$year': '$films.filmShow.dateShow'},
        'recipe': {'$sum': '$films.filmShow.recipe'}
    }},
    {'$sort': {'_id': 1}},
    {'$project': {
        '_id': 0,
        'year': '$_id',
        'recipe': 1
        }
    }
]

result = mongo.db.cinemas.aggregate(pipeline)
data = list(result)


print("Evolution de la recette du cinéma " + cinema + " entre " + start_date.strftime("%Y") + " et " + end_date.strftime("%Y")+ " : ")
for doc in data:
    print("     Année : " + str(doc['year']) + " | Recette : " + str(doc['recipe']) + "€")


# plot the results in histogram
fig, ax = plt.subplots()

y = [doc["recipe"] for doc in data]
x = [doc["year"] for doc in data]

ax.plot(x, y, color='green')

ax.set_xlabel('Année')
ax.set_ylabel('Recette (€)')
ax.set_title('Evolution de la recette du cinéma "' + cinema + '" entre ' + start_date.strftime("%Y") + ' et ' + end_date.strftime("%Y"))

# open window full screen
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

mongo.close()