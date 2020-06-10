# spotify-usage-analysis

I want to find out who I listen to and what their basic background is. Using the Spotify Web API, Python's SpotiPy library and my downloaded data.

## Weighting System
The weighting system used to rank artists is based on data downloaded from Spotify on my usage. It shows how much time I spend listening to a song which I can then use to find how much per artist. 

The per artist weighting system is based on three equally important factors: 
- Average listen time (t)
- Total listens (L)
- Listen recency (R)

***Relevance = t X L X R***

