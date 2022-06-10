from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import requests
from flask import session


class Stock:
    db_stock = 'wealth'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.quantity = data['quantity']
        self.total = data['total']
        self.trader = None
        # self.active = True
        
        

    @classmethod
    def sell_stock(cls, data):
        query = "update stocks SET quantity = %(quantity)s, total=%(total)s WHERE stocks.id = %(id)s;"
        return connectToMySQL(cls.db_stock).query_db(query,data)

#purchase one
    @classmethod
    def new_stock(cls,data):
        query = 'insert into stocks(name,price,user_id, quantity,total) values (%(name)s, %(price)s, %(user_id)s, %(quantity)s, %(total)s);'
        return connectToMySQL(cls.db_stock).query_db(query,data)

    #validate stock
    @staticmethod
    def validate_stock(stock_data):
        valid = True
        if len(stock_data)<1:
            flash('Please enter stock symbol')
            valid = False
        return valid

    #get all
    @classmethod
    def get_all(cls):
        query = 'select * from stocks;'
        results = connectToMySQL(cls.db_stock).query_db(cls)
        all_stocks =[]
        for row in results:
            all_stocks.append(cls(row))
        return all_stocks

    #get all by trader
    @classmethod
    def get_all_by_trader(cls,data):
        query = "select * from stocks JOIN users on user_id = users.id where users.id=%(id)s;"
        results = connectToMySQL(cls.db_stock).query_db(query,data)
        all_stocks = []
        
        for s in results:
            this_stock = cls(s) #stock object

            trader_info = {
                'id' : s['users.id'],
                'first_name' : s['first_name'],
                'last_name' : s['last_name'],
                'email':s['email'],
                'password':s['password'],
                'created_at' : s['created_at'],
                'updated_at' : s['updated_at'],
            }
            this_trader = user.User(trader_info)#user object
            this_stock.trader = this_trader #Instances association
            all_stocks.append(this_stock)#Append the stock containing the associated User to the list of stock
        return all_stocks
            
    
    #get one
    @classmethod
    def get_one(cls,data):
        query = 'select * from stocks where id = %(id)s;'
        results = connectToMySQL(cls.db_stock).query_db(query,data)
        return cls(results[0])


    # get one by trader
    @classmethod
    def get_one_by_trader(cls,data):
        query = "select * from stocks JOIN users on user_id = users.id where stocks .id = %(id)s;"
        results = connectToMySQL(cls.db_stock).query_db(query,data)
        this_stock = cls(results[0])#stock object
        user_data ={
            'id': results[0]['id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['created_at'],
            'updated_at':results[0]['updated_at']
        }
        this_trader = user.User(user_data)#user object

    # @classmethod
    # def update(cls,data):
    #     query = 'update stocks set quantity =%(quantity)s, total=%(total)s, where id=%(id)s;'
    #     return connectToMySQL(cls.db_stock).query_db(query,data)

    @staticmethod
    def api_call(request):
        url = "https://yahoofinance-stocks1.p.rapidapi.com/stock-prices"

        querystring = {"EndDateInclusive":"2022-05-12","StartDateInclusive":"2022-05-12","Symbol":f"{request}","OrderBy":"Ascending"}

        headers = {
            "X-RapidAPI-Host": "yahoofinance-stocks1.p.rapidapi.com",
            "X-RapidAPI-Key": "88e3695b8bmsh42ce67b8bf7a723p1d4abcjsn862b3172e524"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json() # data is an object with all the dictionaries
        
        return {
            'name': request,
            'price':data['results'][0]['adjClose'],
            'user_id': session['user_id']
        }


