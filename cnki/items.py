# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tutor=scrapy.Field()
    school=scrapy.Field()
    paper_name=scrapy.Field()
    paper_link=scrapy.Field()
    author=scrapy.Field()
    publication=scrapy.Field()
    publication_link=scrapy.Field()
    pub_date=scrapy.Field()
    pub_type=scrapy.Field()
    
    short=scrapy.Field()
    dpt=scrapy.Field()
