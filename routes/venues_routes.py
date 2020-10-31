import json
import sys
import logging
from forms import *
from config import db, app, migrate
from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from forms import VenueForm
from model import Venue


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

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.(one Bug)
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  # ilike operator instead of like operator to match case insensitive.
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
