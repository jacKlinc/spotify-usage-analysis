import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy.util as util

client_id = "1971694acef8412ba128e98ef15eacca"
client_secret = "9ba2a9f9a0204c76ac94267790d22c2b"
username = "a2la4jzttvnov9au11hwf56z8"
scope = "user-top-read"
redirect_uri = "http://localhost:8080"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API


token = util.prompt_for_user_token(username,
                           scope,
                           client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        print("range:", range)
        results = sp.current_user_top_artists(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            print(i, item['name'])
        print()
else:
    print("Can't get token for", username)