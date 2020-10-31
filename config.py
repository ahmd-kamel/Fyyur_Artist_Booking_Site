import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_moment import Moment

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# DONE: connect to a local postgresql database and use migration (done)

#... connection to local database called postgres
class DatabaseURI():

    # Just change the names of your database and crendtials and all to connect to your local system
    DATABASE_NAME = "fyyur_db"
    username = 'postgres'
    password = 'Passasdk'
    url = 'localhost:5432'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{url}/{DATABASE_NAME}'


app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseURI.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#... using migration
migrate  = Migrate(app, db, compare_type=True)
# migrate = Migrate(app, db)

