import scrapy
from scrapy.crawler import CrawlerProcess

class WikiSpider(scrapy.Spider):
    """This Spider will find the country of origin and the age of the artist using CSS selector"""
    name = "wiki"
    allowed_domains = ['wikipedia.org'] 
    start_urls = ['https://wikipedia.org/wiki/']

    def __init__(self, artist='', *args, **kwargs):
        """Takes artist as an argument when called"""
        # Replaces spaces with "_" for website
        artist = artist.replace(" ", "_")
        self.start_urls = [f'https://wikipedia.com/wiki/{artist}']

    def parse(self, response):
        """Get artist race"""    
        # Trim brackets and age
        age = response.xpath('/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody/tr[5]/td/span[2]/text()').get()
        age = age.strip(')').lstrip(' (age ')

        country = response.xpath('/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody/tr[6]/td/text()')
    
        yield {
            'country': country,
            'age': age
        }
    
# Setup scraper
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
})

# Instantiate class and pass artist
process.crawl(WikiSpider, artist='21 Savage')
process.start()