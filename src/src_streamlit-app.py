import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import matplotlib.pyplot as plt
import numpy as np
import os
from client_secret import *

def make_df(response):
    """Pass results from Spotfy API call and return cleaned DataFrame"""
    items = pd.DataFrame(response['items'])
    # Drop unnecessary columns
    items = items.drop(['external_urls', 'href', 'id', 'images', 'uri'], axis=1)
    # Followes column needs cleaning
    for i in range(0, len(items)):
        items.followers[i] = items.followers[i]['total']

    items = items.sort_values(by='popularity', ascending=False)
    return items

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
artists.head()

### Title 
st.title("Jack's Spotify Listening")

st.markdown("""This is where I can write 
    my **description** in Markdown.""")

code = '''def hello():
   print("Hello, Streamlit!")'''
st.code(code, language='python')

### Description
st.markdown('# My Spotify App')

### Show head 
st.write('## Spotify Artists DataFrame')
st.write(artists.head(5))

### Plot Favourite Artists
st.write('## Plot Favourite Artists')

# st.bar_chart(artists)
st.bar_chart(artists.name.sort_values(ascending=False), width=50)

fig, ax = plt.subplots(figsize=(15,20))
ax.barh(artists.name, artists.popularity)

st.pyplot()