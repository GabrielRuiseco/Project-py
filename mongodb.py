from pymongo import MongoClient


class MongoConect:
    def __init__(self):
        self.CLIENT = MongoClient(
            "mongodb+srv://Admin:123asterisco@practica1-hjadu.mongodb.net/adonismongo?retryWrites=true&w=majority")

    def create(self, collection, x):
        collection.insert_one(x)

    def search(self, collection, **kwargs):
        self.results = collection.find(kwargs)
        self.all = '\n'.join([str(r) for r in self.results])
        return self.all

    def deleteMongo(self, collection, **kwargs):
        collection.delete_one(kwargs)

    def updateMongo(self, collection, arg1, arg2):
        collection.update_one(arg1, arg2)
        # print(str(arg1), "\n" + str(arg2))

    def deleteMany(self, collection, **kwargs):
        self.keys = collection.delete_many(kwargs)

    def updateMany(self, collection, **kwargs):
        self.keys = collection.update_many(kwargs)