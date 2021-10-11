from types import resolve_bases
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.movies import Movie
from flask import flash

import re


class Review():

    def __init__(self, data):
        self.movie_id = data['movie_id']
        self.user_id = data['user_id']
        self.rating = data['rating']
        self.reason = data['reason']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movie = []


    @classmethod
    def add_review(cls,data):
        query = 'INSERT INTO reviews(movie_id, user_id, rating, reason) VALUES(%(movie_id)s, %(user_id)s, %(rating)s, %(reason)s);'

        results = connectToMySQL('media_schema').query_db(query,data)

        return results

    @classmethod
    def get_all_reviews_by_userid(cls,data):
        query = 'SELECT * FROM movies JOIN reviews ON movies.id = reviews.movie_id JOIN users ON users.id = reviews.user_id WHERE users.id = %(id)s;'

        results = connectToMySQL('media_schema').query_db(query,data)

        reviews =[]
        for review in results:
            single_review = cls(review)
            movie_data = {
                'id': review['id'],
                'name': review['name'],
                'poster':review['poster'],
                'media':review['media'],
                'description': review['description'],
                'created_at': review['created_at'],
                'updated_at': review['updated_at']
            }
            single_review.movie = Movie(movie_data)
            reviews.append(single_review)

        return reviews

    @classmethod
    def get_review_by_id(cls,data):
        query = 'SELECT * FROM movies LEFT JOIN reviews ON movies.id = reviews.movie_id LEFT JOIN users ON users.id = reviews.user_id WHERE user_id = %(user_id)s AND movie_id = %(movie_id)s;'

        results = connectToMySQL('media_schema').query_db(query,data)
        reviews = []
        for review in reviews:
            single_review = cls(review)
            movie_data = {
                'id': review['id'],
                'name': review['name'],
                'poster':review['poster'],
                'media':review['media'],
                'description': review['description'],
                'created_at': review['created_at'],
                'updated_at': review['updated_at']
                }
            single_review.movie = Movie(movie_data)
            review.append(single_review)
        return cls(results[0])

    @classmethod
    def update_review(cls,data):
        query = 'UPDATE reviews SET movie_id = %(movie_id)s, user_id = %(user_id)s, rating = %(rating)s, reason = %(reason)s WHERE user_id = %(user_id)s  AND movie_id = %(movie_id)s;'
        results = connectToMySQL('media_schema').query_db(query,data)

    @classmethod
    def delete_review(cls,data):
        query = 'DELETE FROM reviews WHERE movie_id = %(movie_id)s AND user_id = %(user_id)s;'

        results = connectToMySQL('media_schema').query_db(query,data)

    @classmethod
    def get_all_reviews_by_movieid(cls,data):
        query = 'SELECT * FROM movies LEFT JOIN reviews ON movies.id = reviews.movie_id LEFT JOIN users ON users.id = reviews.user_id WHERE movies.id = %(id)s;'

        results = connectToMySQL('media_schema').query_db(query,data)

        reviews =[]
        for review in results:
            single_review = cls(review)
            movie_data = {
                'id': review['id'],
                'name': review['name'],
                'poster':review['poster'],
                'media':review['media'],
                'description': review['description'],
                'created_at': review['created_at'],
                'updated_at': review['updated_at']
            }
            single_review.movie = Movie(movie_data)
            reviews.append(single_review)

        return reviews

    @classmethod
    def get_all_reviews(cls):
        query = 'SELECT * FROM movies LEFT JOIN reviews ON movies.id = reviews.movie_id LEFT JOIN users ON users.id = reviews.user_id;'

        results = connectToMySQL('media_schema').query_db(query)

        reviews =[]
        for review in results:
            single_review = cls(review)
            movie_data = {
                'id': review['id'],
                'name': review['name'],
                'poster':review['poster'],
                'media':review['media'],
                'description': review['description'],
                'created_at': review['created_at'],
                'updated_at': review['updated_at']
            }
            single_review.movie = Movie(movie_data)
            reviews.append(single_review)

        return reviews