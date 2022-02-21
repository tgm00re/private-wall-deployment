from flask_app.config.mysqlconnection import connectToMySQL
import time
import datetime


class Message:
    def __init__(self, data):
        self.message = data['message'],
        self.sender_id = data['sender_id'],
        self.recipient_id = data['recipient_id']
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message, sender_id, recipient_id, created_at, updated_at) VALUES (%(message)s, %(sender_id)s, %(recipient_id)s, NOW(), NOW() );"
        return connectToMySQL('private-wall').query_db(query, data)

    @classmethod
    def get_recipient_id(cls, data):
        query = "SELECT recipient_id FROM messages WHERE id = %(id)s;"
        result = connectToMySQL('private-wall').query_db(query, data)
        return result[0]['recipient_id']


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL('private-wall').query_db(query, data)