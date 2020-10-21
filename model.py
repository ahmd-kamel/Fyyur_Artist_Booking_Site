from config import db
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #... complete venue model
    genres = db.Column(db.String(120))
    web_site = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    upcoming_shows_count = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    #... relation between show and venue
    venue_show = db.relationship('Show', backref='venue', lazy=True)

    # DONE: implement any missing fields, as a database migration using Flask-Migrate (seem Done)

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #... complete artist model
    web_site = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    upcoming_shows_count = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    #... relation between show and artist
    artist_show = db.relationship('Show', backref='artist', lazy=True)



    # DONE: implement any missing fields, as a database migration using Flask-Migrate (Done)

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime)
  #... Venue foreign key
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  #... Artist foreign key
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  


# DONE Implement Show properties, as a database migration. (done)
