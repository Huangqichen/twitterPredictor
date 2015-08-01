__author__ = 'kahlil'

from classes.ticker import Ticker
import logging
import operator
import time

class DataProc():
    def __init__(self, db):
        self.__db = db
        self.__tickers = Ticker().getTickers()
        self.__words = {}
        self.setup_logger('dplog', r'logs/dp.log')
        self.dplog = logging.getLogger('dplog')

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
            # iterate through every record in the db
            for doc in self.__db.collection.find( {} ):
                tweet = doc['text'].split()
                for word in tweet:
                    wrd = word.lower().strip().encode('utf-8')
                    if wrd in self.__words.keys():
                        logmsg = 'word: {}      in dict: {}     val: {}\n'.format(wrd, self.__words.keys(

                        ).__contains__(wrd), self.__words[wrd])

                        self.dplog.info(logmsg)
                        self.__words[wrd] += 1
                    else:
                        self.__words[wrd] = 1
        except Exception as e:
            msg = '{} {}'.format(doc['id'], e)
            self.dplog.warning(msg)

    def find(self):
        try:
            for doc in self.__db.collection.find(limit=5):
                print doc
        except Exception as e:
            self.dplog.warning(e)

    def getLenWords(self):
        return len(self.__words)

    def getWords(self):
        return sorted(self.__words.items(), key=operator.itemgetter(1), reverse=True)

    def printWords(self):
        for each in self.getWords():
            print each
            #logging.info(each)

    def getSpecialWords(self):
        specialWords = []
        for pair in self.getWords():
            key, value = pair
            if key.startswith("#"):
                specialWords.append(key)

        for word in specialWords:
            print '{}\n'.format(word)

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)
