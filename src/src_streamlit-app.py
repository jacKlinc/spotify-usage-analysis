import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import matplotlib.pyplot as plt
import numpy as np
import os
from client_secret import *
# import requests
# from bs4 import BeautifulSoup as bs4

@st.cache
def scrape_race(artist_name):
    """Get race of artist through web scraping"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    base_url = "https://ethnicelebs.com/"
    
    # Parsed artists name
    parse_name = artist_name.replace(" ", "-")
    req = requests.get(base_url+parse_name, headers=headers)
    soup = bs4(req.content, "html.parser")

    # Find all <p> elements
    para = str(soup.find_all('p'))

    # Find range of string
    string_start = para.find("Ethnicity: ") + len("Ethnicity: ")
    string_end = para.find("</strong")
    race = para[string_start:string_end]

    if len(race) < 100:
        if 'Africa' in race:
            return 'Black'
    else:
        return 'Unknown'

@st.cache
def make_df(response):
    """Pass results from Spotfy API call and return cleaned DataFrame"""
    items = pd.DataFrame(response['items'])
    # Drop unnecessary columns
    items = items.drop(['external_urls', 'href', 'id', 'images', 'uri'], axis=1)
    # Followes column needs cleaning
    for i in range(0, len(items)):
        items.followers[i] = items.followers[i]['total']

    # Sort by popularity
    return items.sort_values(by='popularity', ascending=False)

@st.cache
def spotify_connect(user_scope, redirect_uri, artist_limit, time_range):
    """Connects to Spotify API, returning user's top artists"""
    
    # Load in secret keys
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Create security token
    security_token = util.prompt_for_user_token(username, user_scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
    # Gets favourite artists 
    if security_token:
        spotify_client = spotipy.Spotify(auth=security_token)
        spotify_client.trace = False
        # Loop through time ranges
        for r in time_range:
            results = spotify_client.current_user_top_artists(time_range=r, limit=artist_limit)
        return results 

scope = "user-top-read"
redirect_uri = "http://localhost:8080"

# Get top 10 artists for short, medium and long term
results = spotify_connect(scope, redirect_uri, 10, ['short_term', 'medium_term', 'long_term'])

# Make DataFrame    
artists = make_df(results)

# Read in cached artist information
my_top50_artist_country = pd.read_json('../data/mytop50_artists.json')
top500_artist_country = pd.read_json('../data/top500_spotify_artists.json')


### Title 
st.title("[names]'s Spotify Listening")

'This is a peek at your listening trends'

# Show head
# st.write('## Spotify Artists DataFrame')
# st.write(artists.head(10))

# Plot Favourite Artists
st.write('# Your Top 5')

fig, ax = plt.subplots(figsize=(15,8))
ax.barh(artists.name.head(), artists.popularity.head())
st.pyplot()

# Top artist
artists.head(1).name.iloc[0]+' has the lead'

# races = []
# for artist in artists.name:
#     races.append(scrape_race(artist))

# st.write(races)

# Plot nationalities
st.write("# Where They're from")


# Group artists into countries and sort
countries_group = my_top50_artist_country.groupby('country').artist.count().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(15,8))
ax.bar(countries_group.index, countries_group)
st.pyplot()

countries_group.index[0], ' has the lead'

# Plot ages
st.write("# Age?")
'Here are your favourite age groups'

# Remove 'n/a'
cleaned_df = my_top50_artist_country.loc[my_top50_artist_country.age != 'n/a']

# Define age groups
bins= [0,15,24,35,50,110]
labels = ['0-15', '16-24', '25-35', '36-50', '50+']
cleaned_df['AgeGroup'] = pd.cut(cleaned_df['age'], bins=bins, labels=labels, right=False)

cleaned_df = cleaned_df.sort_values(by='age')

fig, ax = plt.subplots(figsize=(12,5))
ax.bar(cleaned_df['AgeGroup'], cleaned_df.index)
st.pyplot()

cleaned_df['AgeGroup'].max(), ' is in the lead'


### Plot genres
st.write("# Genres")

'You like', cleaned_df['AgeGroup'].max(), ' from',  countries_group.index[0],' in [genre]'