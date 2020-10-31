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
    upcoming_shows = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    past_shows = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    #... relation between show and venue
    venue_show = db.relationship('Show', backref='venue', lazy=True)

    def venue_to_dictionary(self):
      return {
      "id": self.id,
      "name": self.name,
      "city": self.city,
      "state": self.state,
      "address": self.address,
      "phone": self.phone,
      "image_link": self.image_link,
      "facebook_link": self.facebook_link,
      "genres":  self.genres ,
      "web_site": self.web_site,
      "seeking_talent": self.seeking_talent,
      "seeking_description": self.seeking_description,
      "upcoming_shows": self.upcoming_shows,
      "upcoming_shows_count": self.upcoming_shows_count,
      "past_shows": self.past_shows,
      "past_shows_count": self.past_shows_count,
      "venue_show": self.venue_show
      }


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
    upcoming_shows = db.Column(db.Integer)    
    upcoming_shows_count = db.Column(db.Integer)
    past_shows = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    #... relation between show and artist
    artist_show = db.relationship('Show', backref='artist', lazy=True)

    def artist_to_dictionary(self):
      return {
      "id": self.id,
      "name": self.name,
      "city": self.city,
      "state": self.state,
      "phone": self.phone,
      "genres":  self.genres ,
      "image_link": self.image_link,
      "facebook_link": self.facebook_link,
      "web_site": self.web_site,
      "seeking_venue": self.seeking_venue,
      "seeking_description": self.seeking_description,
      "upcoming_shows": self.upcoming_shows,
      "upcoming_shows_count": self.upcoming_shows_count,
      "past_shows": self.past_shows,
      "past_shows_count": self.past_shows_count,
      "artist_show": self.artist_show
      }


    # DONE: implement any missing fields, as a database migration using Flask-Migrate (Done)

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime)
  #... Venue foreign key
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  #... Artist foreign key
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

  def artist_details(self):
    return {
        'artist_id': self.artist_id,
        'artist_name': Artist.query.get(self.artist_id).name,
        'artist_image_link': Artist.query.get(self.artist_id).image_link,
        'start_time': self.start_time
    }

  def venue_details(self):
    return {
      'venue_id': self.venue_id,
      'venue_name': Venue.query.get(self.venue_id).name,
      'venue_image_link': Venue.query.get(self.venue_id).image_link,
      'start_time': self.start_time
    }  
  


# DONE Implement Show properties, as a database migration. (done)
