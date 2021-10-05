# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash 
# model the class after the friend table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('login_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('login_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_schema').query_db(query, data)
        return cls(results[0])
        
    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE emails SET email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
    #     return connectToMySQL('login_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM userss WHERE id = %(id)s"
        return connectToMySQL('login_schema').query_db(query, data)

    @staticmethod
    def validate_email(email):
        is_valid = True
        # test whether a field matches the pattern
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_schema').query_db(query,email)
        if len(results) >= 1:
            flash("Email is taken!")
            is_valid = False
        if not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!")
            is_valid = False
        if email['password'] != email['confirm_password']:
            flash("Passwords don't match!")
            is_valid = False
        return is_valid