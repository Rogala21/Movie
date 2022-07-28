from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
import random

db = "moveis_schema"

class movie: 
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location_watched = data['location_watched']
        self.rating = data['rating']
        self.genre = data['genre']
        self.secondary_genre = data['secondary_genre']
        self.third_genre = data['third_genre']
        self.poster = data['poster']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_added = data['user_added']
        self.watch_later = []
        self.watched = []

    @classmethod
    def new_movie(cls, data):
        query = "INSERT INTO moveis_schema.movies (title, description, location_watched, rating, genre, secondary_genre, third_genre, poster, user_added) VALUES (%(title)s, %(description)s, %(location_watched)s, %(rating)s, %(genre)s, %(secondary_genre)s, %(third_genre)s, %(poster)s, %(user_added)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def edit_movie(cls, data):
        query = "UPDATE moveis_schema.movies SET title = %(title)s, description = %(description)s, location_watched = %(location_watched)s, rating = %(rating)s, genre = %(genre)s, secondary_genre = %(secondary_genre)s, third_genre = %(third_genre)s, poster = %(poster)s WHERE id = %(movie_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_movies(cls):
        query = "SELECT * FROM moveis_schema.movies;"
        results = connectToMySQL(db).query_db(query)
        movies = []
        for movie in results:
            movies.append(cls(movie))
        return movies

    @classmethod
    def add_watch_later(cls, data):
        query = "INSERT INTO moveis_schema.watch_later (movie_id, user_id) VALUES (%(movie_id)s, %(user_id)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def add_watched(cls, data):
        query = "INSERT INTO moveis_schema.watched (dmovie_id, duser_id, user_rating, liked, user_location) VALUES (%(movie_id)s, %(user_id)s, %(user_rating)s, %(liked)s, %(user_location)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def remove_watch_later(cls, data):
        query = "DELETE FROM moveis_schema.watch_later WHERE movie_id = %(movie_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def remove_watched(cls, data):
        query = "DELETE FROM moveis_schema.watched WHERE dmovie_id = %(movie_id)s AND duser_id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_1_movie(cls, id):
        query = "SELECT * FROM moveis_schema.movies where id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {"id": id})
        return cls(results[0])

    @classmethod
    def get_all_movies_movie(cls):
        query = "SELECT * FROM moveis_schema.movies LEFT JOIN moveis_schema.watched ON movies.id = dmovie_id LEFT JOIN moveis_schema.watch_later ON movies.id = watch_later.movie_id;"
        results = connectToMySQL(db).query_db(query)
        movies = []
        for movie in results:
            if len(movies) < 1:
                movies.append(cls(movie))
            current = movies[len(movies)-1]
            if current.id != movie['id']:
                movies.append(cls(movie))
                current = movies[len(movies)-1]
            if movie['dmovie_id'] != None:
                current.watched.append(movie['duser_id'])
            if movie['movie_id'] != None:
                current.watch_later.append(movie['user_id'])
        random.shuffle(movies)
        return movies

    @staticmethod
    def check_stats(data):
        is_valid = True 
        if len(data["title"]) < 1:
            flash(u"Need to enter Movie Title", 'title')
            is_valid = False
        if len(data["description"]) < 1:
            flash(u"Need to enter description", 'description')
            is_valid = False
        if len(data["location_watched"]) < 1:
            flash(u"Need to enter where you watched the movie", 'location_watched')
            is_valid = False
        if len(data["genre"]) < 1:
            flash(u"Need to enter a main genre", 'genre')
            is_valid = False
        if len(data["poster"]) < 1:
            flash(u"Need to enter a poster link", 'poster')
            is_valid = False
        return is_valid

class movie_watched: 
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location_watched = data['location_watched']
        self.rating = data['rating']
        self.genre = data['genre']
        self.secondary_genre = data['secondary_genre']
        self.third_genre = data['third_genre']
        self.poster = data['poster']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_added = data['user_added']
        self.watch_later = []
        self.watched = []
        self.user_rating = data['user_rating']
        self.user_location = data['user_location']
        self.liked = data['liked']

    @classmethod
    def get_all_movies_watched(cls):
        query = "SELECT * FROM moveis_schema.movies LEFT JOIN moveis_schema.watched ON movies.id = dmovie_id;"
        results = connectToMySQL(db).query_db(query)
        movies = []
        for movie in results:
            if len(movies) < 1:
                movies.append(cls(movie))
            current = movies[len(movies)-1]
            if current.id != movie['id']:
                movies.append(cls(movie))
                current = movies[len(movies)-1]
            if movie['dmovie_id'] != None:
                current.watched.append(movie['duser_id'])
        return movies