from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = []

# *******- selects all shows and shows in dashboard -*
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(DATABASE).query_db(query)
        shows = []
        for r in results:
            print(r)
            shows.append(cls(r))
        return shows

# *******- creates/inserts one show 
    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES (%(title)s, %(network)s, %(release_date)s,%(description)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# *******- gets the one show from the one user -**
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows left join users on shows.user_id = users.id where shows.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        one_show = cls(result[0])

        user_data = {
                "id" : result[0]["users.id"],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }

        one_show.owner = user_model.User(user_data)
        return one_show

# *******- Updates/edits the sshow  -
    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title=%(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- deletes the show -*
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- allows the show selected to be displayed -*  
    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validates_show_creation_updates(data):
        is_valid = True
# *******- validates Show title 
        if len(data['title']) == 0:
            flash("Please provide a show title!")
            is_valid = False
        elif len(data["title"]) < 3:
            flash("title name must be at least three characters")
            is_valid = False

# *******- validates shows -***
        if len(data['network']) == 0:
            flash("Please provide a network!")
            is_valid = False
        elif len(data["network"]) < 3:
            flash("Network must be at least three characters")
            is_valid = False

# *******- validates show date that was seen -
        if  not data['release_date']:
            flash("Date required!")
            is_valid = False
# *******- validates show date that was seen *            
        if len(data['description']) == 0:
            flash("Please provide a show description!")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("description must be at least three characters")
            is_valid = False

        return is_valid

# *******- get_user_with_shows holds the user and its shows *
    @classmethod
    def get_user_with_shows( cls , data ):
        query = "SELECT * FROM users LEFT JOIN shows ON users.id = shows.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )

        user = cls( results[0] )
        for row in results:

            show_data = {
                "id" : row['id'],
                "title" : row['title'],
                "network" : row['network'],
                "release_date" : row['release_date'],
                "description" : row['description'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['user_id']
            }
            user.users.append(Show(show_data))
        return user
