print(__name__)
if __name__ == "classes.mongodb": from . import config
else: import config
from pymongo import MongoClient

class MongoDb:
    def __init__(self):
        client = MongoClient(config.mongoDb)  #tempcollect DB
                
        # Check our DB exists else create it
        self.db = client[config.database]
        # Check our collection exists else create it
        self.collection = self.db[config.collection]

    def add(self, record):
        self.collection.insert_one(record)  

    def get(self, filter):
        return self.collection.find(filter)

# Used for testing
# mongo = MongoDb()
# # mongo.add({'city': 'Firbeix', 'temp': 8.1})
# print(mongo.get({'city': 'Firbeix'}))
# for temp in mongo.get({'city': 'Firbeix'}):
#     print(temp['date'], temp['temp'])