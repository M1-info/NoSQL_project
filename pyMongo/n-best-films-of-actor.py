import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

nb_films = 3
actor = {
    'firstName': 'Daniel',
    'lastName': 'Radcliffe'
}

pipeline = [
    {'$unwind': '$actors'},
    {'$match': {'actors': actor}},
    {'$unwind': '$feedbacks'},
    {'$group': {
        '_id': '$title',
        'average_rating': {'$avg': '$feedbacks.rating'},
    }},
    {'$sort': {'average_rating': -1}},
    {'$limit': nb_films}
]

result = mongo.db.films.aggregate(pipeline)

print("Les " + str(nb_films) + " films les mieux notés de " + actor['firstName'] + " " + actor['lastName'] + " sont : \n")
for doc in result:
    print("Film : " + doc['_id'] + " (" + str(doc['average_rating']) + "/5)")