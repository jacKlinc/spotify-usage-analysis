import scrapy
from scrapy.crawler import CrawlerProcess

class EthnicCelebSpider(scrapy.Spider):
    """Scrapes example ethnic celebs website using XPath selector"""
    name = "ethnic_celebs"

    def __init__(self, artist='', **kwargs):
        """Takes artist as an argument when called"""
        # Replaces spaces with "-" for website
        artist = artist.replace(" ", "-")
        self.start_urls = [f'https://ethnicelebs.com/{artist}']

    def parse(self, response):
        """Get artist race"""    
        next_page = response.xpath('/html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong/text()').get()
        # Find word and exclude
        string_start = next_page.find("Ethnicity: ") + len("Ethnicity: ")
        race = next_page[string_start:len(next_page)]
        
        print('\n'+race+'\n')
        return race


