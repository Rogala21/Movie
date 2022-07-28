from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

db = "moveis_schema"

class user_follow: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.following_id = []
        self.follower_id = []

    @classmethod
    def new_following(cls, data):
        query = "INSERT INTO moveis_schema.following (follower_id, following_id) VALUES (%(follower_id)s, %(following_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def un_following(cls, data):
        query = "DELETE FROM moveis_schema.following where follower_id = %(follower_id)s AND following_id = %(following_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM moveis_schema.users LEFT JOIN moveis_schema.following ON id = follower_id WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        following = []
        for user in results:
            if len(following) < 1:
                following.append(cls(user))
            current = following[len(following) - 1]
            if current.id != user['id']:
                following.append(cls(user))
                current = following[len(following) - 1]
            if user['following_id'] != None:
                current.following_id.append(user['following_id'])
        return following[0]

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM moveis_schema.users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_all_user_following(cls, id):
        query = "SELECT * FROM moveis_schema.users LEFT JOIN moveis_schema.following ON id = follower_id WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {"id": id})
        users = []
        for user in results:
            if len(users) < 1:
                users.append(cls(user))
            current = users[len(users) - 1]
            if current.id != user['id']:
                users.append(cls(user))
                current = users[len(users) - 1]
            if user['following_id'] != None:
                current.following_id.append(user['following_id'])
        return users

    @classmethod
    def get_all_user_followers(cls, id):
        query = "SELECT * FROM moveis_schema.users LEFT JOIN moveis_schema.following ON id = following_id WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {"id": id})
        users = []
        for user in results:
            if len(users) < 1:
                users.append(cls(user))
            current = users[len(users) - 1]
            if current.id != user['id']:
                users.append(cls(user))
                current = users[len(users) - 1]
            if user['follower_id'] != None:
                current.follower_id.append(user['follower_id'])
        return users[0]

    @classmethod
    def get_all_following(cls, ids):
        query = "SELECT * FROM moveis_schema.users where id in {};".format(ids)
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users