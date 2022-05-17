# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

from flask_app import DATABASE






class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email  = data['email']
        self.password  = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @property
    def fullname(self:dict) -> object:
        """
        this function will return an f string that will have the full name
        """
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"




# C
    @classmethod
    def create(cls, data:dict) -> object:
        """
        inserting data into the users table
        this is the request.form
        """
        #query string
        query = "INSERT INTO users(first_name, last_name , email , password ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        #contact the DB
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        # return
        return user_id



# R
    @classmethod
    def get_one(cls, data:dict) -> list:
        """
        selecting one from the users table
        """
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        # Create an empty list to append our instances of friends
        if results:
            return cls(results[0])
        return False




    # Now we use class methods to query our database
    @classmethod
    def get_all(cls:dict) -> object:
        """
        selecting all from the users table
        """
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        if results:
            users = []
        # Iterate over the db results and create instances of friends with cls.
            for user in results:
                users.append( cls(user) )
            return users
        return False

#GETTING EMAIL FOR LOGIN
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])




# U
    @classmethod
    def update_one(cls, data:dict) -> None:
        """
        updating one from the users table
        """
        query = "UPDATE first_name SET first_name = %(first_name)s WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)




# D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        """
        delete one from the users table
        """
        query = "DELETE FROM first_name WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)









# VALIDATIONS BELOW
# USER
    @staticmethod
    def validate(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("Name must have at least 3 characters.", "error_user_first_name")
            is_valid = False
        if len(user['last_name']) < 2:
            flash(" Last Name must have at least 3 characters.", "error_user_last_name")
            is_valid = False
            
        if len(user['email']) < 1:
            flash("Have to put a valid email", "error_user_email")
            is_valid = False
            
            
        if len(user['password']) < 8:
            flash("Put at least 8 characters in the password box.", "error_user_password", "error_user_valid_password")
            is_valid = False
        if len(user['confirm_password']) < 8:
            flash("Confirm password is a required field!", "error_user_confirm_password")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Has to match the first password")
            is_valid = False
        return is_valid

# EMAIL VALID
    @staticmethod
    def validate_email(user):
        is_valid = True # we assume this is true
        query = "SELECT email FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, user)
        if len(results) >= 1:
            flash("Too late that email is taken")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email aint real bro")
            is_valid = False
        return is_valid