from DotEnv import DotEnv
from pymongo import MongoClient
from pymongo.database import Database
from pprint import pprint

class Mongo:

    client: MongoClient
    db: Database
    
    def __init__(self) -> None:
        DotEnv.load()

        mongo_env = DotEnv.get_by_prefix('MONGO_')

        self.client = MongoClient(
            mongo_env['MONGO_HOST'], 
            int(mongo_env['MONGO_PORT']), 
            username=mongo_env['MONGO_USER'], 
            password=mongo_env['MONGO_PASSWORD'], 
            authSource=mongo_env['MONGO_DB'], 
            authMechanism='SCRAM-SHA-1'
        )

        self.db = self.client[mongo_env['MONGO_DB']]

    def print_cursor(self, cursor):
        for document in cursor:
            pprint(document)


    def close(self):
        self.client.close()