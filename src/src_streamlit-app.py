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

## Gather and store functions
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
            user = spotify_client.current_user()
            if 'display_name' in user:
                name = user['display_name']
        return results, name

## Grouping plot functions
def get_country_groups(top50_df):
    """Pass Top 50 artists and returns country group of those artists"""
    # Remove 'n/a'
    remove_nas = top50_df.loc[top50_df.country != 'n/a']
    # Group artists into countries and sort
    return remove_nas.groupby('country').artist.count().sort_values(ascending=False)

def get_age_groups(top50_df):
    """Pass Top 50 artists and returns age group of those artists"""
    # Remove 'n/a'
    cleaned_df = top50_df.loc[top50_df.age != 'n/a']

    # Define age groups
    bins= [0,15,24,35,50,110]
    labels = ['0-15', '16-24', '25-35', '35-50', '50+']
    return pd.cut(cleaned_df['age'], bins=bins, labels=labels, right=False)

def grade_genre(genre, total):
    """Pass genre and total of genres, returns percent graded genre"""
    return (genre/total) * 100

def get_genres(df):
    """Pass artists df and returns graded genre dict"""
    # Init genre values
    rock=rap=pop=house=funk=folk=RandB=jazz=classical=electronic=0
    # Loop over each artist
    for genres in df.genres:
        # Loop through artist's list of genres
        for genre in genres:
            if 'rap' in genre or 'hip hop' in genre:
                rap+=1
            elif 'pop' in genre:
                pop+=1
            elif 'rock' in genre:
                rock+=1
            elif 'funk' in genre:
                funk+=1
            elif 'house' in genre or 'techno' in genre:
                house+=1
            elif 'folk' in genre or 'country' in genre:
                folk+=1
            elif 'r&b' in genre or 'rhythm' in genre:
                RandB+=1
            elif 'jazz' in genre:
                jazz+=1
            elif 'classical' in genre:
                classical+=1
            elif 'electronic' in genre:
                electronic+=1 
    
    # Find sum of all genres
    total = rock+rap+pop+house+funk+folk+RandB+jazz+classical+electronic
    
    # Pass genre and total to percent grade
    return {
        'rap': grade_genre(rap, total),
        'pop': grade_genre(pop, total),
        'rock': grade_genre(rock, total),
        'funk': grade_genre(funk, total),
        'techno/house': grade_genre(house, total),
        'country/folk':grade_genre(folk, total),
        'r&b': grade_genre(RandB, total),
        'jazz': grade_genre(jazz, total),
        'classical': grade_genre(classical, total),
        'electronic': grade_genre(electronic, total)
    }


scope = "user-top-read"
redirect_uri = "http://localhost:8080"

# Get top 10 artists for short, medium and long term
results, name = spotify_connect(scope, redirect_uri, 100, ['short_term', 'medium_term', 'long_term'])

# Make DataFrame    
artists = make_df(results)

# Read in cached artist information
my_top50_artist_country = pd.read_json('../data/mytop50_artists.json')
top500_artist_country = pd.read_json('../data/top500_spotify_artists.json')


# Title 
name, "'s Spotify Listening"
'This is a peek at your listening trends'

# Plot Favourite Artists
st.write('# Your Top 5')

fig, ax = plt.subplots(figsize=(15,8))
ax.barh(artists.name.head(), artists.popularity.head())
st.pyplot()

# Top artist
artists.head(1).name.iloc[0]+' has the lead'

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

age_groups = get_age_groups(my_top50_artist_country)

fig, ax = plt.subplots(figsize=(12,5))
ax.bar(age_groups, age_groups.index)
st.pyplot()

age_groups.max(), ' is in the lead'


### Plot genres
st.write("# Genres")

genres = get_genres(artists)

fig, ax = plt.subplots(figsize=(14,4))
ax.bar(genres.keys(), genres.values())
st.pyplot()

'You like', age_groups.max(), ' from', countries_group.index[0],' in the ', max(genres, key=genres.get), 'genre'