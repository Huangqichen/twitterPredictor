__author__ = 'kahlil'

from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient
import time
from classes.ticker import Ticker
import logging
logging.basicConfig(filename='logs/msl.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

class MyStreamListener(StreamListener):

    def __init__(self):
        super(MyStreamListener, self).__init__()
        self.__tweet = ''
        self.__languages = 'en'
        self.__tickers = Ticker()
        self.__trackList = self.__tickers.getTickers()

    def on_data(self, data):
        while json.loads(data) != self.__tweet:
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
                logging.warning(e)
                pass

    def on_error(self, status):
        print(status)
        if status == 420:
            time.sleep(60)

    def getTracklist(self):
        return self.__trackList
