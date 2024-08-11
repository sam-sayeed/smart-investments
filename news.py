import json

import requests

NEWS_API_KEY = 'eb8ec5bd8630400a8bdc73a0c184388f'

class News:
    def __init__(self,company):
        self.company = company

    def getNews( self ) :
        param = {
            'q' : self.company,
            'apiKey' : NEWS_API_KEY
        }
        response = requests.get('https://newsapi.org/v2/everything', params = param)
        response.raise_for_status()
        data = response.json()['articles'][:3]
        # data = self.__getNewsList()['articles'][:3]
        newsObj = self.__createObj(data)
        return  newsObj

    @staticmethod
    def __getNewsList():
        with open('newsDB.json', 'r',encoding="utf8") as file :
            data = json.load(file)
        return data

    @staticmethod
    def __createObj( data ) :
        result = []
        temp = {}
        for i in data :
            temp['title'] = i['title']
            ds = i['description'][:50] + '....'
            temp['description'] = ds
            temp['url'] = i['url']
            result.append(temp)
        return result

