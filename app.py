#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
import logging
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import db, app, migrate
from model import Venue, Artist, Show



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Done: num_shows should be aggregated based on number of upcoming shows per venue.(seem Done)
  
  #...  not dynamic with events 
  #...  define an empty lists to store the data
  city_and_state = []
  data = []

  #... all venus on the same city and state
  venue_table = Venue.query.all()
  #... itrate on all rows in the query
  for row in venue_table:
    if city_and_state == row.city + row.state:
      data[len(data) - 1]["venues"].append({
        "id": row.id,
        "name": row.name,
        "upcoming_shows_count": row.upcoming_shows_count
      })
      
    else:
      city_and_state = row.city + row.state
      data.append({"city": row.city, "state": row.state,
          "venues": [{"id": row.id, "name": row.name,
          "upcoming_shows_count": row.upcoming_shows_count }]
          })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.(one Bug)
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get("search_term", "")
  venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
  upcoming_shows = 0

  response={
    "count": len(venues),
    "data": [{
      "id": venue.id,
      "name": venue.name,
      #here is a bug
      "num_upcoming_shows": 0,
    }
    for venue in venues
    ]
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id (2 bugs)

  venue = Venue.query.get(venue_id)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.web_site,
    "facebook_link": venue.facebook_link,
    # here is boolean bug
    "seeking_talent": True,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    # here there is add bug
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    # here there is add bug
    "upcoming_shows": [],
    "past_shows_count": venue.past_shows_count,
    "upcoming_shows_count": venue.upcoming_shows_count,

  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data = []
  artists = Artist.query.all()
  for artist in artists:
     data.append({
       "id": artist.id,
       "name": artist.name
     })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get("search_term", "")
  artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  response={
    "count": len(artists),
    "data": [{
      "id": artist.id,
      "name": artist.name,
      #here is a bug
      "num_upcoming_shows": artist.upcoming_shows_count,
    }
    for artist in artists
    ]
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.get(artist_id)
  data={
    "id": artist_id,
    "name": artist.name,
    "genres": [artist.genres],
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.web_site,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    # buggy
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    #buggy
    "upcoming_shows": [],
    "past_shows_count": artist.past_shows_count,
    "upcoming_shows_count": artist.past_shows_count,
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  artist={
    "id": artist_id,
    "name": artist.name,
    "genres": [artist.genres],
    "city": artist.city,
    "state": artist.city,
    "phone": artist.phone,
    "website": artist.web_site,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  venue={
    "id": venue_id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.city,
    "phone": venue.number,
    "website": venue.web_site,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  form = ArtistForm()
  error = False

  name = form.name.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  image_link = form.image_link.data
  genres = form.genres.data
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data
  website = form.website.data
  facebook_link = form.facebook_link.data

  try:
    artist = Artist(name=name, city=city, state=state,
    phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link,
    website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()  
  if error:
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = Show.query.all()
  for show in shows:
    data.append({
    "venue_id": show.venue.id,
    "venue_name": show.venue.name,
    "artist_id": show.artist.id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  form = ShowForm()
  error = False

  artist_id = form.artist_id.data
  venue_id = form.venue_id.data
  start_time = form.start_time.data
  print(venue_id)

  try:
    show = Show(start_time=start_time, artist_id=artist_id, venue_id=venue_id)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')


  # on successful db insert, flash success
  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
