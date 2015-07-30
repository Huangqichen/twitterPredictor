__author__ = 'kahlil'

import tweepy
from tweepy import Stream
from classes.oauth import OAuth
from classes.myStreamListener import MyStreamListener
from classes.ticker import Ticker
import logging
logging.basicConfig(filename='logs/tc.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

try:
    t = Ticker()
    oa = OAuth()
    auth = tweepy.OAuthHandler(oa.getConsumerKey(), oa.getConsumerSecret())
    auth.set_access_token(oa.getAccessToken(), oa.getAccessTokenSecret())

    api = tweepy.API(auth)
    l = MyStreamListener()
    stream = Stream(auth, l)

    for chunk in t.chunkTickers():
        stream.filter(track=chunk, async=True)
except Exception as e:
    logging.warning(e)
