__author__ = 'kahlil'
import mysql.connector
from bs4 import BeautifulSoup
import urllib2
import mysql.connector
import logging
logging.basicConfig(filename='logs/ticker.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

class Ticker:
    def __init__(self):
        self.__config = {
        'user': 'root',
        'password': '!qazXsw2#edc',
        'host': 'localhost',
        'port': '3306',
        'database': 'securities',
        'raise_on_warnings': True,}
        self.__cnxn = mysql.connector.connect(**self.__config)
        self.__cursor = self.__cnxn.cursor()
        self.__tickerList = []
        self.scrapeTickers()

    def scrapeTickers(self):
        # create list of tickers
        url2scrape = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        page = urllib2.urlopen(url2scrape).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        table = soup.find("table", { "class" : "wikitable sortable" })

        for row in table.findAll("tr")[1:]:
            self.__tickerList.append(row.a.string)

        for ticker in self.__tickerList:
            tableCreate = 'CREATE TABLE IF NOT EXISTS tickers (' \
                          'ID int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT, ' \
                          'TICKER VARCHAR(5));'
            addTicker = "INSERT INTO tickers (ticker) VALUE ('{}');".format(ticker)
            try:
                #self.__cursor.execute(tableCreate)
                self.__cursor.execute(addTicker)
                self.__cnxn.commit()
            except Exception as e:
                logging.warning(e)
                print e
                pass
            else:
                self.__cnxn.close

    def getTickers(self):
        tickers = []
        for ticker in self.__tickerList:
            tickerProc1 = '#{}'.format(ticker)
            tickerProc2 = '${}'.format(ticker)
            tickers.append(tickerProc1)
            tickers.append(tickerProc2)
        tickers = sorted(tickers)
        return tickers

    def chunkTickers(self):
        chunks=[self.getTickers()[x:x+200] for x in xrange(0, len(self.getTickers()), 200)]
        return chunks