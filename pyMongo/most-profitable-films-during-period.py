import sys
sys.path.append('../utils')

from MongoDB import Mongo
from datetime import datetime

mongo = Mongo()

start_date = datetime(2010, 1, 1)
end_date = datetime(2010, 12, 31)
nb_dates = 5

pipeline = [
    {'$match': {'$and': [{'releaseDate': {'$gte': start_date}}, {'releaseDate': {'$lte': end_date}}]}},
    {'$group': {
        '_id': '$releaseDate',
        'films': {'$push': '$$ROOT'}
    }},
    {'$project': {
        '_id': 0, 
        'releaseDate': {'$dateToString': {'format': '%d-%m-%Y', 'date': '$_id'}},
        'films.recipe': 1, 
        'films.numberEntries': 1, 
        'films.title': 1
    }},
    {"$sort": {"films.recipe": -1}},
    {"$limit": nb_dates}
]

result = mongo.db.films.aggregate(pipeline)

print("Les films les plus rentables sont pour la période du "+ start_date.strftime("%d-%m-%Y") +" au "+ end_date.strftime("%d-%m-%Y") +" sont : \n")
for doc in result:
    print("Films sortis le " + doc['releaseDate'] + " : \n")
    for film in doc['films']:
        print("     Film : " + film['title'])
        print("     Recette totale : " + str(film['recipe']) + "€")
        print("     Nombre d'entrées total : " + str(film['numberEntries']))
        print("")

mongo.close()