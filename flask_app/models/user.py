from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import stock

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name ='wealth'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.stocks = []
        

#create user
    @classmethod
    def create(cls,data):
        query = 'insert into users(first_name,last_name,email,password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    #validate user
    @staticmethod
    def validate_user(form_data):
        valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,form_data)
        if len(results)>0:
            flash("Email already taken")
            valid = False
        if len(form_data['first_name'])<2:
            flash("Name must be at least two characters")
            valid = False 
        if len(form_data['last_name'])<2:
            flash("Last name must be at least two characters")
            valid = False 
        if form_data['password'] != form_data['confirm']:
            flash("Passwords need to match")
            valid = False
        if len(form_data['password'])< 8:
            valid = False
            flash('Password must be at least 8 characters long')
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Please enter valid email address")
            valid = False
        return valid

    #get user by email
    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) ==0:   #to check if the user is in the db
            return False
        if len(results)>=1:
            valid = False
        return cls(results[0])

    #get user by id
    @classmethod
    def get_by_id(cls,data):
        query = 'select * from users where id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])




