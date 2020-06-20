import scrapy
from scrapy.crawler import CrawlerProcess

## Check the domain/robots.txt which defines the limitations of scraping

## ScraPy Shell
#   - Navigate to root scrapy project
#   - scrapy shell myUrl
#   - response.css('h2::text').get(): returns first h2 element on page
#   - response.css('.post-header').get(): returns first instance of class on page
#   - response.css('.post-header a::text').get(): returns first instance of class on page
#   - response.css('p::text').re(r'scraping'): finds RegEx in paragraph element

## Using XPath
#   - response.xpath('//h3/text()').getall(): returns all h2s
#   - Using the console you can copy the XPath by clicking on it
#   - ethnic: /html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong

class EthnicCelebSpider(scrapy.Spider):
    """Scrapes example web page using CSS selector"""
    name = "ethnic_celebs"
    start_urls = [
        'https://ethnicelebs.com/21-savage'
    ]

    def parse(self, response):
        """Get artist race"""     
        next_page = response.xpath('/html/body/div/div/div/div/div/section/div[2]/article/div/div[2]/div[1]/p[4]/strong/text()').get()
        # Find word and exclude
        string_start = next_page.find("Ethnicity: ") + len("Ethnicity: ")
        race = next_page[string_start:len(next_page)]
        
        print('\n'+race+'\n')
        return race


# Setup scraper
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

# Instantiate class
process.crawl(EthnicCelebSpider, artist='21 savage')
process.start()