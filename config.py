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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Passasdk@localhost:5432/fyyur_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#... using migration
migrate  = Migrate(app, db, compare_type=True)
# migrate = Migrate(app, db)

