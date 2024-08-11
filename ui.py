import tkinter as tk
from tkinter import *
from tkinter import messagebox as ms
# import requests
from DB import UserInfo
from stock import Stockdata
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
GREEN = "#9bdeac"
from DB import COMPANY_CODE
user_email = ''
FNAME = ''
LNAME = ''
company = ''
class UserInterface:
    def __init__(self):
        self.db = UserInfo()
        window = Tk()
        bg = PhotoImage(file='C:/Users/sayee/Desktop/work/image89.png')
        window.title('Smart Investments')
        # window.config(padx=50, pady=50, bg=YELLOW)
        window.geometry('1000x650')
        
        
        canvas = Canvas(window, width=1000,height=650)
        canvas.pack(fill='both',expand=True)
        canvas.create_image(0,0,image=bg,anchor='nw')
        canvas.create_text(500,100,text='Smart Investments', font=(FONT_NAME, 60, 'bold'), fill='#45FFCA')
        
        canvas.create_text(240,200,text='First Name: ', font=(FONT_NAME, 20, 'bold'), fill='white')
        canvas.create_text(230,280,text='Last Name: ', font=(FONT_NAME, 20, 'bold'), fill='white')
        canvas.create_text(200,360,text='Email: ', font=(FONT_NAME, 20, 'bold'), fill='white')
        canvas.create_text(215,440,text='Company: ', font=(FONT_NAME, 20, 'bold'), fill='white')
        
        self.fname_input = Entry(window, width=30, font=('Helvetica', 18),bd=0)
        self.lname_input = Entry(window, width=30, font=('Helvetica', 18),bd=0)
        self.email_input = Entry(window, width=30, font=('Helvetica', 18),bd=0)
        
        option = [i for i in COMPANY_CODE.keys()]
        option = sorted(option)
        self.temp_company = StringVar()
        self.temp_company.set('Select From Below')
        company_option = OptionMenu(window,self.temp_company,*option)
        company_option.config(width=53,padx=20, pady=5,bd=0)
        
        fname_window = canvas.create_window(350,183,anchor='nw',window=self.fname_input)
        lname_window = canvas.create_window(350,263,anchor='nw',window=self.lname_input)
        email_window = canvas.create_window(350,343,anchor='nw',window=self.email_input)
        company_window = canvas.create_window(350,423,anchor='nw',window=company_option)
        
        
        canvas.create_text(550,480,text='(Please change company and resubmit for multiple subscription)', font=('Helvetica', 12, 'italic'), fill='#E21818')
        
        
        sbStart_button = Button(text='Subscribe', command=self.subscription_submit, width=20, background='#007bff',fg='white')
        sb_btn_window = canvas.create_window(150,530,anchor='nw',window=sbStart_button)
        sb_end_button = Button(
            text='Unsubscribe', command=self.unsubscription_submit, width=20, background='#007bff',fg='white')
        sbEnd_btn_window = canvas.create_window(400,530,anchor='nw',window=sb_end_button)
        end_button = Button(
            text='Exit', command=window.destroy, width=20, background='#007bff',fg='white')
        end_btn_window = canvas.create_window(650,530,anchor='nw',window=end_button)
        

        window.mainloop()
    def is_data_valid(self,c,f,l,e):
        print(c,f,l,e)
        if c not in COMPANY_CODE.keys():
            ms.showerror('ERROR!',message = 'Please select a company')
            return False
        if e.count('@') != 1:
            ms.showerror('ERROR!', message = 'Please provide a proper email')
            return False
        if not f or not l:
            ms.showerror('ERROR!', message = 'Name cannot  be empty')
            return False

        return True

    def subscription_submit(self):
        user_email = self.email_input.get()
        FNAME = self.fname_input.get()
        LNAME = self.lname_input.get()
        company = self.temp_company.get()
        print(FNAME, LNAME, company, user_email,COMPANY_CODE[company])
        print(self.is_data_valid(company,FNAME,LNAME,user_email))
        if self.is_data_valid(company,FNAME,LNAME,user_email):
            self.db.add_subscriber(company = COMPANY_CODE[company],name = FNAME+' '+LNAME,email = user_email)
            ms.showinfo(title = 'Confirmation',
                        message = 'Thank you for being a subscriber. You will get updated daily on the stock price.')
            Stockdata().getDataForGivenCompany(company)
        else:
            ms.showinfo('Failed',message = 'Subscription process failed!')
        # store_userInfo()
        # stock_info()

    def unsubscription_submit(self):

        user_email = self.email_input.get()
        FNAME = self.fname_input.get()
        LNAME = self.lname_input.get()
        company = self.temp_company.get()
        print(FNAME, LNAME, company, user_email)
        if self.is_data_valid(company, FNAME, LNAME, user_email) :
            is_removed = self.db.remove_subscriber(company = company,name = FNAME+ ' ' + LNAME,email = user_email)
            if is_removed:
                ms.showinfo(title = 'Confirmation',
                            message = 'Unsubscribed successfully! We are sorry to see you go.')
            else:
                ms.showinfo('Failed', message = 'Unsubscription process failed!')
    #     check whether user exist or  not then remove.


