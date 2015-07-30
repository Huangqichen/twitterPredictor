__author__ = 'kahlil'

from classes.ticker import Ticker
from nltk import FreqDist
import nltk
import logging
import operator
logging.basicConfig(filename='logs/dp.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

class DataProc():
    def __init__(self, db):
        self.__db = db
        self.__tickers = Ticker().getTickers()
        self.__words = {}

    def totalCount(self):
        pipe = [ { '$group': {'_id': None,
                      'count': { '$sum': 1 } } } ]
        for doc in self.__db.collection.aggregate(pipeline=pipe):
            return doc['count']

    def tickerCounts(self):

        for ticker in self.__tickers:
            pipeTicker = [ {'$match': { '$text': { '$search': ticker } } },
                        { '$group': {'_id': None, 'count': { '$sum': 1 } } } ]
            for doc in self.__db.collection.aggregate(pipeline=pipeTicker):
                avg = float(doc['count']) / self.totalCount()
                print 'total records matching {} {} out of {} = {:.2%}'.format(ticker, doc['count'],
                                                                                 self.totalCount(), avg)

    def processTweetText(self):
        try:
            for doc in self.__db.collection.find( {} ):
                tweet = doc['text'].split()
                for word in tweet:
                    wrd = word.lower().strip().encode('utf-8')
                    if wrd in self.__words.keys():
                        logmsg = 'word: {}      in dict: {}     val: {}\n'.format(wrd, self.__words.keys(

                        ).__contains__(wrd), self.__words[wrd])
                        logging.info(logmsg)
                        self.__words[wrd] += 1
                    else:
                        self.__words[wrd] = 1
        except Exception as e:
            logging.warning(e)

    def getLenWords(self):
        return len(self.__words)

    def getWords(self):
        sorted_x = sorted(self.__words.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_x:
            print each
            logging.info(each)