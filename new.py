import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://ye:1234@cluster0.z0dtg.mongodb.net/<dbname>?retryWrites=true&w=majority')

db = cluster['test']
collection = db['test']

{'_id': 0, 'name': 'ye', 'score': 5}

collection.insert_one({})