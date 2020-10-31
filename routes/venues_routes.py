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
from model import Venue, Show, Artist
from filters import format_datetime


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
  # DONE: replace with real venue data from the venues table, using venue_id (2 bugs)

  venue = Venue.query.get(venue_id)
  if venue:
    data = venue.venue_to_dictionary()
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
      "seeking_talent": True,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
    }

    current_time = datetime.now().strftime('%Y-%m-%d')

    new_shows_query = Show.query.options(db.joinedload('artist')).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
    new_show = list(map(Show.artist_details, new_shows_query))
    data["upcoming_shows"] = new_show
    data["upcoming_shows_count"] = len(new_show)
    past_shows_query = Show.query.options(db.joinedload('artist')).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
    past_shows = list(map(Show.artist_details, past_shows_query))
    data["past_shows"] = past_shows
    data["past_shows_count"] = len(past_shows)

    return render_template('pages/show_venue.html', venue=data)
  else:
    return render_template('errors/404.html')
    


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
    "phone": venue.phone,
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
  # LASTXX: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  name = form.name.data
  city = form.city.data
  state = form.state.data
  address = form.address.data
  phone = form.phone.data
  genres = form.genres.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  website = form.website.data
  seeking_talent = True if form.seeking_talent.data == 'Yes' else False
  seeking_description = form.seeking_description.data 

  if not form.validate():
    flash( form.errors )
    return redirect(url_for('edit_venue_submission', venue_id=venue_id))

  else:
    error_in_update = False
    try:
      venue = Venue.query.get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone

      venue.seeking_talent = seeking_talent
      venue.seeking_description = seeking_description
      venue.image_link = image_link
      venue.website = website
      venue.facebook_link = facebook_link
      venue.genres = genres
      db.session.commit()
    except:
      error_in_update = True
      print(f'Exception "{e}" in edit_venue_submission()')
      db.session.rollback()  
    finally:
      db.session.close()

    if not error_in_update:
      # on successful db update, flash success
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_venue', venue_id=venue_id))

    else:
      flash('An error occurred. Venue ' + name + ' could not be updated.')
      print("Error in edit_venue_submission()")
      return render_template('errors/500.html')
  


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
