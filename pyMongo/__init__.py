from ..utils.MongoDB import Mongo

mongo = Mongo()

db = mongo.db

collections = db.list_collection_names()

print(collections)

mongo.close()