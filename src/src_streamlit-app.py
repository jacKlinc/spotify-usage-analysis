import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import matplotlib.pyplot as plt
import numpy as np
import os
from client_secret import *

scope = "user-top-read"
redirect_uri = "http://localhost:8080"

# Load in secret keys
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create security token
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Gets favourite artists 
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        # Limited to 50 artists over all time ranges
        results = sp.current_user_top_artists(time_range=r, limit=50)

# Add to DataFrame
name=[]
popularity=[]
genres=[]
followers=[]

for artist in results['items']:
    if len(artist['genres']) > 0:
        # Append each to list
        name.append(artist['name'])
        popularity.append(artist['popularity'])
        followers.append(artist['followers']['total'])
        
        # Adds genres in CSV
        csv_genre=''
        for genre in artist['genres']:
            csv_genre+=genre+','
        genres.append(csv_genre)

# Add list to DataFrame
artists = pd.DataFrame()
artists['name'] = name
artists['popularity'] = popularity
artists['followers'] = followers
artists['genre'] = genres

artists = artists.sort_values(by='popularity', ascending=False)

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