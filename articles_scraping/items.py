# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlesScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Authors
    authors_name = scrapy.Field()
    authors_university = scrapy.Field()
    authors_country = scrapy.Field()
    
    # Article
    title = scrapy.Field()
    topic = scrapy.Field()
    doi = scrapy.Field()
    date_publication = scrapy.Field()
    keywords = scrapy.Field()
    abstract_ = scrapy.Field()
    references = scrapy.Field()
    downloads = scrapy.Field()
    citations = scrapy.Field()

    # Journal
    journal_name = scrapy.Field()
    issn = scrapy.Field()
    impact_factor = scrapy.Field()
    indexation = scrapy.Field()
    
    pass
