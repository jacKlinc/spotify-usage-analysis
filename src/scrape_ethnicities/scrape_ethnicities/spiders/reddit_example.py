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

class RedditSpider(scrapy.Spider):
    """Scrapes example web page using CSS selector"""
    name = "posts"
    start_urls = [
        'https://blog.scrapinghub.com/page/1/'
    ]

    def parse(self, response):
        """Loop through page for post title, data and author"""
        # Writes to JSON file
        # page = response.url.split('/')
        # filename = 'posts-%s.json' % page
        # with open(filename, 'wb') as file:
        #     file.write(response.body)
        for post in response.css('div.post-item'): 
            # yield is like return
            yield {
                # Gets title, date and author
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get()
            }
        # Gets link of class
        next_page = response.css('a.next-posts-link::attr(href)').get()
        # Checks if not None
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



