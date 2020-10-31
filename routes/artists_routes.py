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
from forms import ArtistForm
from model import Artist, Show, Venue


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
  # DONE: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.get(artist_id)
  if artist:
    data = artist.artist_to_dictionary()
    data={
      "id": artist.id,
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
    }

    current_time = datetime.now().strftime('%Y-%m-%d')
    new_shows_query = Show.query.options(db.joinedload('artist')).filter(Show.artist_id == artist_id).filter(Show.start_time >= current_time).all()
    new_show = list(map(Show.venue_details, new_shows_query))
    data["upcoming_shows"] = new_show
    data["upcoming_shows_count"] = len(new_show)
    past_shows_query = Show.query.options(db.joinedload('artist')).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
    past_shows = list(map(Show.venue_details, past_shows_query))
    data["past_shows"] = past_shows
    data["past_shows_count"] = len(past_shows)

    return render_template('pages/show_artist.html', artist=data)
  else:
    return render_template('errors/404.html')


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
