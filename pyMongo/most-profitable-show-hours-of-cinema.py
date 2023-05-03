import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

pipeline = [
    {'$unwind': '$films'},
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

print("Statistique des heures de projection les plus rentables :")
for doc in result:
    print("Heure : {}h".format(doc['_id']))
    print("     Recette : {}€".format(doc['recipe']))
    print("     Nombre d'entrées : {}".format(doc['numberEntries']))
    print("     Nombre de séances : {}".format(doc['numberShows']))
    print("     Nombre moyen d'entrées par séance : {}".format(doc['enterPerShow']))
    print()