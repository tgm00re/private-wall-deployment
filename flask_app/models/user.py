import datetime
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at'],
        self.messages_sent = 0
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL('private-wall').query_db(query, data)

    @classmethod
    def get_all_but_self(cls, data):
        query = "SELECT * FROM users WHERE id <> %(id)s;"
        results = connectToMySQL('private-wall').query_db(query, data)
        users = []
        for user in results:
            users.append( cls(user) )
        print("PRINTING ALL BUT SELF")
        return users

    
    # List of Dictionaries:
    # { 
    #    "message": (message)
    #   "sender_first": sender_first
    #   "created_at": created_at
    # }
    @classmethod
    def get_associated_messages(cls, data):
        query = "SELECT users2.first_name as sender_first, messages.message as message, messages.created_at as created_at, messages.id as message_id FROM users LEFT JOIN messages ON users.id = messages.recipient_id LEFT JOIN users AS users2 ON messages.sender_id = users2.id WHERE users.id = %(id)s;"
        results = connectToMySQL('private-wall').query_db(query, data)
        messagesData = []
        for row_in_db in results:
            f = '%Y-%m-%d %H:%M:%S'   
            datetime.datetime.strptime(str(row_in_db['created_at']), f)
            now = datetime.datetime.now()
            now.strftime(f)
            delta = now - row_in_db['created_at']
            time_unit = "seconds"
            delta = delta.total_seconds()
            if(delta > 86400):
                delta = delta/86400
                time_unit = "days"
            elif(delta > 3600):
                delta = delta/3600
                time_unit = "hours"
            elif(delta > 60):
                delta = delta/60
                time_unit = "minutes"
            delta = str(delta).split(".")[0]
            messageData = {
                "message": row_in_db['message'],
                "sender_first": row_in_db['sender_first'],
                "delta": delta,
                "message_id": row_in_db['message_id'],
                "time_unit": time_unit
            }        
            messagesData.append(messageData)
        return messagesData

    @classmethod
    def get_total_received(cls, data):
        query = "SELECT COUNT(messages.message) as count FROM messages WHERE recipient_id = %(id)s"
        result = connectToMySQL('private-wall').query_db(query, data)
        return result[0]['count']


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('private-wall').query_db(query,data)

        if len(result) < 1:
            return False #Nobody with that email.
        return cls(result[0])


    @staticmethod
    def validate_user(user):
        is_valid = True
        if not user['first_name'].isalpha() or len(user['first_name']) < 1:
            flash("First Name Must Be Alphabetic And Not Left Empty!" ,'register')
            is_valid = False
        if not user['last_name'].isalpha() or len(user['last_name']) < 1:
            flash("Last Name Must Be Alphabetic And Not Left Empty!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please Input A Valid Email Address", 'register')
            is_valid = False
        if len(user['password']) < 5:
            flash("Passwords Must Be 5 Or More Characters", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Your Passwords Didn't Match", 'register')
            is_valid = False
        return is_valid