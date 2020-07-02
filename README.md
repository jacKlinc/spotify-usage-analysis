# Spotify Usage Analysis

I want to find out who I listen to and what their basic background is. 
Using Spotify and MusicBrainz's APIs to get the data and Streamlit to display it in a dashboard.

- The analysis of the data above will be done in Jupyter notebooks and available in the **/notebooks** directory.
- The Streamlit application is in the **/src** directory


## Spotify Web API
This API gives access to a user's data and can be used within Python. 
When authenticating, the user's username and password must be entered before accessing the information.

## MusicBrainz API
Music Brainz has one of the largest online metadata set for music artists. 
It also has a Python library which is pretty easy to use but has rate limiting, 
only letting me search for an artist once a second.

- This can be overcome by caching my favourite artists in a local JSON file.
- When testing with new users, the top 10k artists will be cached also

## Streamlit App
After analysing and graphing the data in Jupyter, the visualisations will be 
added to a dashboard for the user to see their favourite artists.

- The contents and layout are yet to be designed
- Recommendations for new artists could be added too


## Weighting System
The weighting system used to rank artists is based on data downloaded from Spotify on my usage. It shows how much time I spend listening to a song which I can then use to find how much per artist. 

The per artist weighting system is based on three equally important factors: 
- Average listen time (t)
- Total listens (L)
- Listen recency (R)

***Relevance = t X L X R***
