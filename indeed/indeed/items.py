# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    JobTitle = scrapy.Field()
    JobUrl = scrapy.Field()
    JobID = scrapy.Field()
    Company = scrapy.Field()
    Location = scrapy.Field()
    Salary = scrapy.Field()
    PostDate = scrapy.Field()

class JobItem(scrapy.Item):
    #PageUrl = scrapy.Field()
    Description = scrapy.Field()
    JobID = scrapy.Field()
    pass
