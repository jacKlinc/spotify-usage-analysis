# -*- coding: utf-8 -*-
# import pandas as pd
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import spotipy.util as util
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# from client_secret import *
import scrapy
from scrapy.crawler import CrawlerProcess

class EthnicScraperSpider(scrapy.Spider):
    """Scrapes ethnic celebs website using XPath selector"""
    name = 'ethnic-scraper'
    allowed_domains = ['ethnicelebs.com'] 
    start_urls = ['https://ethnicelebs.com/']

    def __init__(self, artists=[], *args, **kwargs):
        """Takes artist as an argument when called"""
        # super(EthnicScraperSpider, self).__init__(*args, **kwargs)
        # # Replaces spaces with "-" for website
        # artist = artist.replace(" ", "-")
        # self.start_urls = [f'https://ethnicelebs.com/{artist}']
        for artist in artists:
            super(EthnicScraperSpider, self).__init__(*args, **kwargs)
            # Replaces spaces with "-" for website
            artist = artist.replace(" ", "-")
            self.start_urls.append([f'https://ethnicelebs.com/{artist}'])

    def parse(self, response):
        """Get artist race"""
        next_page = response.xpath('/html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong/text()').get()
        # Find word and exclude
        # string_start = next_page.find("Ethnicity: ") + len("Ethnicity: ")
        # race = next_page[string_start:len(next_page)]
        
        yield {
            'race': next_page
        } 


# def make_df(response):
#     """Pass results from Spotfy API call and return cleaned DataFrame"""
#     items = pd.DataFrame(response['items'])
#     # Drop unnecessary columns
#     items = items.drop(['external_urls', 'href', 'id', 'images', 'uri'], axis=1)
#     # Followes column needs cleaning
#     for i in range(0, len(items)):
#         items.followers[i] = items.followers[i]['total']

#     # Sort by popularity
#     return items.sort_values(by='popularity', ascending=False)

# def spotify_connect(user_scope, redirect_uri, artist_limit, time_range):
#     """Connects to Spotify API, returning user's top artists"""
    
#     # Load in secret keys
#     client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     # Create security token
#     security_token = util.prompt_for_user_token(username, user_scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
#     # Gets favourite artists 
#     if security_token:
#         spotify_client = spotipy.Spotify(auth=security_token)
#         spotify_client.trace = False
#         # Loop through time ranges
#         for r in time_range:
#             results = spotify_client.current_user_top_artists(time_range=r, limit=artist_limit)
#         return results
    

# scope = "user-top-read"
# redirect_uri = "http://localhost:8080"

# # Get top 10 artists for short, medium and long term
# results = spotify_connect(scope, redirect_uri, 10, ['short_term', 'medium_term', 'long_term'])

# # Make DataFrame    
# artists = make_df(results)


# for art in artists:
# Setup scraper
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'FEED_FORMAT': 'json',
    'FEED_URI': '123.json',
    'CONCURRENT_ITEMS': 1
})

crawler = process.create_crawler(EthnicScraperSpider)
process.crawl(crawler, artists=['21-savage'])
process.start()