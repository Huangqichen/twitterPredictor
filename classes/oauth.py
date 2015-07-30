__author__ = 'kahlil'

class OAuth:
    def __init__(self):
        self.__consumer_key = 'flYXLw7NTdCDenCd1DoWb3MAU'
        self.__consumer_secret = 'vb12z4w6y43ANJrw4PdKPSm0eBqMtah7OphQ06NIj4QDpdc3w8'
        self.__access_token = '14376815-0PieneMg4hRFD7ZH0OE5vVXB9xd1pUGGVp1cxS6Nb'
        self.__access_token_secret = 'OQeZedwzYmi2HNWN1cqZO4y3weAkvOEs7iKH19lusKKZw'

    def getConsumerKey(self):
        return self.__consumer_key

    def getConsumerSecret(self):
        return self.__consumer_secret

    def getAccessToken(self):
        return self.__access_token

    def getAccessTokenSecret(self):
        return self.__access_token_secret
