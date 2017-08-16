# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field

class OneArticle(Item):
    """docstring for OneArticle"""
    title = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
