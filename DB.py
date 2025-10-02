import json
COMPANY_CODE = {
    'Tesla' : 'TSLA',
    'Apple' : 'AAPL',
    'JP Morgan' : 'JPM',
    'Meta' : 'META',
    'Amazon': 'AMZN',
    'Alphabet' : 'GOOG',
    'Microsoft' : 'MSFT'
}

class UserInfo:
	def __init__(self):
		self.data = self.__read_json()


	def __read_json( self ):
		data = None
		try :
			with open('saved-subscription.json', 'r') as file :
				data = json.load(file)
		except FileNotFoundError :
			print('Json file is empty. Creating a new record.')
			with open('saved-subscription.json', 'w') as file :
				json.dump({}, file, indent = 4)
		return data if data else {}

	def __write_json( self ):
		with open('saved-subscription.json', 'w') as file :
			json.dump(self.data, file, indent = 4)

	def add_subscriber( self,company,name,email ):
		dt = {email: name}
		checker = self.data.get(company)
		if checker:
			self.data[company].append(dt)
		else:
			temp = [dt]
			self.data[company] = temp
		self.__write_json()
		print('User Added...')
	def remove_subscriber( self, company,name,email ):
		# Need to send back a confirmation of successful or fail removal.
		dt = {email:name}
		tempData = self.data.get(company)
		if tempData:
			t =self.__is_subscriber(tempData,dt)
			index = t[1]
			checker = t[0]
			if checker:
				tempData.pop(index)
				self.data[company] = tempData
				self.__write_json()
				#self.__read_json()
				print('User Removed....')
				return True
			else :
				print('No User exist with given information')
				return False
		else:
			print('No User exist with given information')
			return False

	def __is_subscriber( self,tempDB, dt ):
		ind = -1
		for i in range(len(tempDB)):
			if tempDB[i] == dt:
				ind = i
				return True,ind
		return False,ind

	def getSubscriberList( self,company ):
		print(company,self.data.get(company))
		return self.data.get(company, None)