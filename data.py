import pymongo
from pymongo import MongoClient
cluster = MongoClient('localhost', 27017)

db = cluster.FitnessCenter
collection = db.visitors

names = collection.find({})
list_of_names = list()
for i in names:
    list_of_names.append(i['name'])