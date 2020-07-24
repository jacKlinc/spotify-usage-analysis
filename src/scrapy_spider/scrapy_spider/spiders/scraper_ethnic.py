# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess


class EthnicScraperSpider(scrapy.Spider):
    """Scrapes ethnic celebs website using XPath selector"""
    name = 'ethnic-scraper'
    allowed_domains = ['ethnicelebs.com'] 

    def __init__(self, artist='', *args, **kwargs):
        """Takes artist as an argument when called"""
        super(EthnicScraperSpider, self).__init__(*args, **kwargs)
        # Replaces spaces with "-" for website
        artist = artist.replace(" ", "-")
        self.start_urls = [f'https://ethnicelebs.com/{artist}']

    def parse(self, response):
        """Get artist race"""
        next_page = response.xpath('/html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong/text()').get()
        # Find word and exclude
        string_start = next_page.find("Ethnicity: ") + len("Ethnicity: ")
        race = next_page[string_start:len(next_page)]
        
        yield {
            'race': race
        } 
# Setup scraper
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'FEED_FORMAT': 'json',
    'FEED_URI': '123.json',
    'CONCURRENT_ITEMS': 1
})

crawler = process.create_crawler(EthnicScraperSpider)
process.crawl(crawler, artist='21 savage')
process.start()