import json

import requests
from DB import UserInfo,COMPANY_CODE
from news import News
from emailCLI import EmailClient

# STOCK_NAME = "TSLA"
# COMPANY_NAME = "Tesla Inc"
# 'LXPSK9EUVRAQOXEB' --> 'OP9ZCNBHME335W8J' --> 'YS173QYNHVV7D905'
STOCK_API_KEY = 'YS173QYNHVV7D905'
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
        'function' : 'TIME_SERIES_DAILY',
        'symbol' : '',
        'apikey' : STOCK_API_KEY
    }
class Stockdata:
	def __init__(self):
		self.com_info = COMPANY_CODE
		# self.get_stock_data()

	def get_stock_data( self ):
		for i in self.com_info.keys():
			sub = UserInfo().getSubscriberList(self.com_info[i])
			if sub:
				stock_params['symbol'] = self.com_info[i]
				response = requests.get(STOCK_ENDPOINT,stock_params )
				response.raise_for_status()
				stock_data = response.json().get('Time Series (Daily)')
				print(stock_data)
				if stock_data:
					# stock_data = self.__readStockDB()['Time Series (Daily)']
					temp_key = self.__get_first_two_keys(stock_data)
					last_open_price = float(stock_data[temp_key[0]]['1. open'])
					last_closing_price = float(stock_data[temp_key[0]]['4. close'])
					diff,diff_percent,up_down = self.__findPriceDifference(last_open_price,last_closing_price)
					# print(diff,diff_percent,up_down, self.com_info[i])
					company_sub = UserInfo().getSubscriberList(self.com_info[i])
					if company_sub:
						news_obj = News(i).getNews()
						EmailClient(news_obj,i,company_sub,up_down,diff,diff_percent,last_open_price,last_closing_price)
					# print(news_obj)
					# print(company_sub)

	
	def getDataForGivenCompany(self,company):
		sub = UserInfo().getSubscriberList(self.com_info[company])
		if sub:
			stock_params['symbol'] = self.com_info[company]
			response = requests.get(STOCK_ENDPOINT,stock_params )
			response.raise_for_status()
			stock_data = response.json().get('Time Series (Daily)')
			if stock_data:
				# stock_data = self.__readStockDB()['Time Series (Daily)']
				temp_key = self.__get_first_two_keys(stock_data)
				last_open_price = float(stock_data[temp_key[0]]['1. open'])
				last_closing_price = float(stock_data[temp_key[0]]['4. close'])
				diff,diff_percent,up_down = self.__findPriceDifference(last_open_price,last_closing_price)
				# print(diff,diff_percent,up_down, self.com_info[i])
				company_sub = UserInfo().getSubscriberList(self.com_info[company])
				if company_sub:
					news_obj = News(company).getNews()
					EmailClient(news_obj,company,company_sub,up_down,diff,diff_percent,last_open_price,last_closing_price)


	@staticmethod
	def __get_first_two_keys( st ) :
		i = 0
		res = []

		for key in st.keys():
			res.append(key)
			i += 1
			if len(res) == 2:
				break
		return res

	@staticmethod
	def __readStockDB() :

		with open('stockdb.json', 'r') as file :
			data = json.load(file)
		return data

	@staticmethod
	def __findPriceDifference( open_price, closing_price ) :
		diff = round(open_price - closing_price,2)
		up_down = None
		if diff > 0 :
			up_down = " ++ "
		else :
			up_down = " -- "
		# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
		diff_percent = round((abs(diff) / (float(open_price)) * 100),2)
		return diff,diff_percent,up_down



