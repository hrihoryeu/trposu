import pymongo
from pymongo import MongoClient 

cluster = MongoClient('mongodb+srv://Yegor:1234@cluster0.z0dtg.mongodb.net/<dbname>?retryWrites=true&w=majority')

db = cluster['FitnessCenter']
collection = db['visitors']

names = collection.find({})
list_of_names = list()
for i in names:
    list_of_names.append(i['name'])