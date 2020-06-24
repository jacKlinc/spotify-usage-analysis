import scrapy
from scrapy.crawler import CrawlerProcess

class EthnicCelebSpider(scrapy.Spider):
    """Scrapes ethnic celebs website using XPath selector"""
    name = "ethnic_celebs_p"

    def __init__(self, artist='', **kwargs):
        """Takes artist as an argument when called"""
        # for artist in artists:
        # Replaces spaces with "-" for website
        # artist = artist.replace(" ", "-")
        print(artist)
        self.start_urls.append([f'https://ethnicelebs.com/{artist}'])
        
    def parse(self, response):
        """Get artist race"""    
        if response.status != 404:
            next_page = response.xpath('/html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong/text()').get()
            # Find word and exclude
            string_start = next_page.find("Ethnicity: ") + len("Ethnicity: ")
            race = next_page[string_start:len(next_page)]
        else:
            race = 'Unknown'
        
        print('\n'+race+'\n')
        return race

# Setup scraper
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' 
})

# Instantiate class and pass artist
process.crawl(EthnicCelebSpider, artist='21_savage')
process.start()