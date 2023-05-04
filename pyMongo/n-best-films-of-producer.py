import sys
sys.path.append('../utils')

from MongoDB import Mongo

mongo = Mongo()

nb_films = 3
producer = {
    'firstName': "David",
    'lastName': "Heyman",
}

pipeline = [
    {'$unwind': '$producers'},
    {'$match': {'producers': producer}},
    {'$unwind': '$feedbacks'},
    {'$group': {
        '_id': '$title',
        'average_rating': {'$avg': '$feedbacks.rating'},
    }},
    {'$sort': {'average_rating': -1}},
    {'$limit': nb_films}
]

result = mongo.db.films.aggregate(pipeline)

print("Les " + str(nb_films) + " films les mieux notés de " + producer['firstName'] + " " + producer['lastName'] + " sont : \n")
for doc in result:
    print("Film : " + doc['_id'] + " (" + str(doc['average_rating']) + "/5)")

mongo.close()