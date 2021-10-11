from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

class User():

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls,data):
        query = 'INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        results = connectToMySQL('media_schema').query_db(query,data)

        return results

    @classmethod
    def check_database_for_email_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'

        results = connectToMySQL('media_schema').query_db(query,data)

        emails =[]

        for email in results:
            emails.append(User(email))
        return emails

    @classmethod
    def get_user_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'

        results = connectToMySQL('media_schema').query_db(query,data)

        user =[cls(results[0])]

        return user

    @staticmethod
    def validate_registration(user):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid=True

        if len(User.check_database_for_email_by_email(user)) != 0:
            flash('Email already exists')
            is_valid=False

        if not email_regex.match(user['email']):
            flash('Invalid email address')
            is_valid=False

        if len(user['password']) < 3 or len(user['password']) > 45:
            flash('Your password must be between 3 and 45 characters')
            is_valid=False

        if user['password'] != user['confirmPassword']:
            flash("Passwords don't match")
            is_valid= False

        if len(user['first_name']) == 0 or len(user['first_name']) > 45:
            flash('First name must be between 1 and 45 characters')
            is_valid=False

        if len(user['last_name']) == 0 or len(user['last_name']) > 45:
            flash('Last name must be between 1 and 45 characters')
            is_valid=False
        
        return is_valid

