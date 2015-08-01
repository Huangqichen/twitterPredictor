__author__ = 'kahlil'

from classes.ticker import Ticker
from pymongo import MongoClient
from tweepy.streaming import StreamListener
import json
import time
import logging

class MyStreamListener(StreamListener):

    def __init__(self):
        super(MyStreamListener, self).__init__()
        self.__tweet = ''
        self.__languages = 'en'
        self.__tickers = Ticker()
        self.__trackList = self.__tickers.getTickers()
        self.setup_logger('msllog', r'logs/msl.log')
        self.msllog = logging.getLogger('msllog')

    def on_data(self, data):
        try:
            client = MongoClient('localhost', 27017)
            db = client['twitter_db']
            collection = db['twitter_collection']
            self.__tweet = json.loads(data)
            self.__tweetText = self.__tweet['text'].encode('ascii','ignore').strip()

            # keyList = []
            # keys = open('keys.txt', 'w')
            # for key in self.__tweet.keys():
            #     if key not in keyList:
            #         keyList.append(key)
            #         keys.write(key)
            #         keys.write('\n')
            # keys.close()

            # extract data from tweet
            insertion = {}
            fieldsToExtract = ['id','timestamp_ms','text','favorited','favorite_count','retweeted',
                               'retweet_count','coordinates','geo']
            for field in self.__tweet:
                if field in fieldsToExtract and self.__tweet['lang'] == self.__languages:
                    insertion[field] = self.__tweet[field]

                    # build word dictionary for record
                    rd = self.buildRecordDict()
                    insertion['rd'] = rd

            if insertion:
                # write to file
                # saveFile = open('raw_tweets.json', 'w+')
                # saveFile.write(data)
                # saveFile.write('\n')
                # saveFile.close()

                # insert tweet into mongodb
                print insertion
                collection.insert(insertion)

        except Exception as e:
            self.msllog.warning(e)
            pass

    def on_error(self, status):
        print(status)
        if status == 420:
            time.sleep(60)

    def buildRecordDict(self):
        try:
            recordDict = {}
            tweet = self.__tweetText.split()
            for word in tweet:
                wrd = word.lower().strip().encode('utf-8')

                if '.' in wrd:
                    wrd = wrd.replace('.', '')
                if '$' in wrd:
                    wrd = wrd.replace('$', '')

                if wrd in recordDict.keys():
                    recordDict[wrd] += 1
                else:
                    recordDict[wrd] = 1

            return recordDict

        except Exception as e:
            msg = '{} {}'.format(self.__tweet['id'], e)
            self.msllog.warning(msg)

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
