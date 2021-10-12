from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask import flash


class Movie():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.poster = data['poster']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.media = data['media']
        self.user = []


    @classmethod
    def add_movie(cls,data):
        query = 'INSERT INTO movies(name, description, poster, media) VALUES(%(name)s, %(description)s, %(poster)s, %(media)s);'

        results = connectToMySQL('media_schema').query_db(query,data)

        return results

    @classmethod
    def get_all_movies(cls):
        query = 'SELECT * FROM movies WHERE media = "movie";'

        results = connectToMySQL('media_schema').query_db(query)

        movie_list = []

        for single_movie in results:
            x = cls(single_movie)
            movie_list.append(x)

        return movie_list

    @classmethod
    def get_all_animes(cls):
        query = 'SELECT * FROM movies WHERE media = "anime";'

        results = connectToMySQL('media_schema').query_db(query)

        movie_list = []

        for single_movie in results:
            x = cls(single_movie)
            movie_list.append(x)

        return movie_list

    @classmethod
    def get_all_books(cls):
        query = 'SELECT * FROM movies WHERE media = "book";'

        results = connectToMySQL('media_schema').query_db(query)

        movie_list = []

        for single_movie in results:
            x = cls(single_movie)
            movie_list.append(x)

        return movie_list

    @classmethod
    def get_all_books(cls):
        query = 'SELECT * FROM movies WHERE media = "book";'

        results = connectToMySQL('media_schema').query_db(query)

        movie_list = []

        for single_movie in results:
            x = cls(single_movie)
            movie_list.append(x)

        return movie_list

    @classmethod
    def get_movie_by_id(cls,data):
        query = 'SELECT * FROM movies WHERE id = %(id)s'

        results = connectToMySQL('media_schema').query_db(query,data)

        single_movie = cls(results[0])

        return single_movie

    @classmethod
    def get_movie_by_name(cls,data):
        query = 'SELECT * FROM movies WHERE name = %(name)s'

        results = connectToMySQL('media_schema').query_db(query,data)

        movies = []
        for movie in results:
            movies.append(Movie(movie))
        return movies

    @staticmethod
    def movie_validate(data):
        is_valid = True
    
        if len(Movie.get_movie_by_name(data)) != 0:
            is_valid = False
        return is_valid