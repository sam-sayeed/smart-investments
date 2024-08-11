import smtplib as sm
APP_EMAIL = 'stockfluctuation@gmail.com'
APP_PASSWORD = 'airk enmn rlol okth'




class EmailClient:
	def __init__( self,news_list, company_name,user_list,sign,price_diiferenc, pri_difference_percent,opn_price,clos_price ):
		self.news_list = news_list
		self.user_list = user_list
		self.company_name = company_name
		self.sign = sign
		self.price_change = price_diiferenc
		self.change_percent = pri_difference_percent
		self.open_price = opn_price
		self.close_price = clos_price
		self.send_email()

	def send_email( self) :
		for i in self.user_list:
			email = list(i.keys())[0]
			name = list(i.values())[0]

			MSG = self.create_email_body(name)
			self.send_email_to_user(MSG,email)

	def create_email_body(self,name) :
		msg =f'Subject: {self.company_name} price changed by {self.change_percent}%{self.sign}\n\n'
		msg += (f'Hi {name},\nThese is a change in price of the {self.company_name} stock.\nYesterday Closing: ${self.close_price},\nToday Opening: ${self.open_price}.\n\n'
		        f'Below some news headlines and link you might be interested:\n\n'
		        f'{self.news_list[0]["title"]} , Part of Description: {self.news_list[0]["description"]}, URL: {self.news_list[0]["url"]}\n')
		return msg

	def send_email_to_user( self, MSG,email ) :
		print (MSG, email)
		connection = sm.SMTP('smtp.gmail.com')
		connection.starttls()
		connection.login(user = APP_EMAIL, password = APP_PASSWORD)
		connection.sendmail(from_addr = APP_EMAIL, to_addrs = email,
							msg = MSG)
		connection.close()