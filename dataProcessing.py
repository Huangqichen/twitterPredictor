__author__ = 'kahlil'

from classes.db import Db
from classes.dataProc import DataProc

d = Db()
dp = DataProc(d)
print dp.totalCount()
#dp.tickerCounts()
dp.processTweetText()
print dp.getLenWords()
print dp.getWords()