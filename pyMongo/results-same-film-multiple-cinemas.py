import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

film = 'Arbre durer'

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

print("Résultats pour le film \"" + film + "\" :\n")
for doc in result:
    print("Cinema \"" + doc['name'] + "\" :")
    print("     Nombre de séances : " + str(doc['numberSessions']))
    print("     Prix moyen séance: " + str(doc['average_price']) + "€")
    print("     Recette : " + str(doc['recipe']) + "€")
    print("     Nombre d'entrées : " + str(doc['numberEntries']))
    print("")

mongo.close()
