__author__ = 'kahlil'

from classes.db import Db
from classes.dataProc import DataProc

d = Db()
dp = DataProc(d)
#d.db.drop_collection('twitter_collection')
#d.collection.reindex()
#print d.collection.index_information()
print dp.totalCount()
#dp.tickerCounts()
#dp.processTweetText()
#print dp.getLenWords()
#print dp.getSpecialWords()
dp.find()