__author__ = 'kahlil'
from pymongo import MongoClient

class Db():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['twitter_db']
        self.collection = self.db['twitter_collection']
