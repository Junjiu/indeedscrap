#Written by Zane Witherspoon
#9/22/2014
#Web scraping a yelp page for name, rating, number of reviews, and hours
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from indeed.items import IndeedItem, JobItem
from scrapy.selector import Selector
import re

class indeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["indeed.com",]
    start_urls = [
        "http://www.indeed.com/m/jobs?q=data&l="
    ]
    head = "http://www.indeed.com/m"
    ID_match = re.compile('(?<=jk\=)[0-9a-zA-Z]*$')

    def parse(self, response):     #the initializating/only method
        
        #Declairing the scraped item items.py contains IndeedListing()
        nextpage = Selector(response).xpath('/html/body/p[12]/a/@href').extract()[-1]
        yield scrapy.Request(self.head + '/' + nextpage, callback=self.parse)
        for sel in response.xpath('//body/p'):
            item = IndeedItem()
            item['JobTitle'] = sel.xpath('./a/text()').extract()
            item['JobUrl'] = sel.xpath('./a/@href').extract()[0]
            url = item['JobUrl']
            try:
                item['JobID'] = re.search(self.ID_match, url).group(0)
                print(item['JobID'])
            except:
                continue
            item['Location'] = sel.xpath('./span[@class="location"]/text()').extract()
            item['Company'] = sel.xpath('./text()').extract()
            item['PostDate'] = sel.xpath('./span[@class="date"]/text()').extract()
            item['Salary'] = sel.xpath('./span[@class="salary"]/text()').extract()
            if item['JobTitle'] and item['Location']:
                yield item
            if item['Location'] and item['JobUrl']:
                yield scrapy.Request(self.head + '/'+ url,
                                    callback=self.parse_job_details)


    def parse_job_details(self, response):
        item = JobItem()
        url = response._get_url()
        item['JobID'] = re.search(self.ID_match, url).group(0)
        item['Description'] = response.xpath('//div[@id="desc"]/text()' +
                            '[preceding-sibling::br or preceding-sibling::p]'
                            ).extract()
        return item


