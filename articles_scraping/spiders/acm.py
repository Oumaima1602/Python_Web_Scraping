from typing import Any, Optional
import scrapy
from scrapy_splash import SplashRequest
from articles_scraping.items import ArticlesScrapingItem

class AcmSpider(scrapy.Spider):
    name = "acm"
    topic = "None"
    allowed_domains = ["dl.acm.org"]
    start_urls = []

    handle_httpstatus_list = [302]
    handle_httpstatus_list = [301]

    def __init__(self, keyword = None, topic=None, *args, **kwargs):
        super(AcmSpider, self).__init__(*args, **kwargs)
        #self.start_urls = ['https://dl.acm.org/action/doSearch?AllField=' + topic ]
        for i in range(50):
            self.start_urls += ['https://dl.acm.org/action/doSearch?AllField=' + topic + '&startPage=' + str(i) + '&pageSize=' + str(20)]

        self.topic = topic

    def parse(self, response):
        for article in response.css("a::attr(href)"):
            if'/doi/' in article.extract():
                yield SplashRequest('https://dl.acm.org' + article.extract(), self.parse_article, args={'wait': 3})

    def parse_article(self, response):
        item = ArticlesScrapingItem()

        # ----------- Déclaration ----------- #
        #Article
        title = response.css('.citation__title::text').extract_first()
        topic = self.topic
        doi = response.css('.issue-item__doi::text').extract()
        date_publication = response.css('.CitationCoverDate::text').extract()
        abstract_ = response.css('.abstractSection').css('p::text').extract()
        references = response.css('.references__note::text').extract()
        downloads = ';'.join(response.css('.tooltip .metric').css('span::text').extract())
        citations = ';'.join(response.css('.tooltip .citation').css('span::text').extract())

        # Authors
        authors_name = response.css('.author-data').css('span::text').extract()
        authors_infos = response.css('.author-info__body').css('p::text').extract()
        authors_university = []
        authors_country = []

        if len(authors_infos) != 0:
            for auth_info in authors_infos:
                if auth_info != "":
                    s = auth_info.split(',')
                    authors_university.append(s[0])

                    if len(s) > 1:
                        authors_country.append(s[len(s) - 1])
                    else:
                        authors_country = ""
                else:
                    authors_university = ""
                    authors_country = ""

        authors_country = ';'.join(authors_country)

        # Journal
        publisher = "ACM"
        issn = "00045411; 1557735X"
        impact_factor = 6.738
        indexation = 134

        # ----------- Affectation ----------- #
        # Article Affectation
        item['title'] = title
        item['topic'] = topic
        item['doi'] = doi[0]

        try:
            item['date_publication'] = int(date_publication[0].split(' ')[-1])
        except:
            item['date_publication'] = 0

        item['abstract_'] = abstract_
        item['references'] = references

        item['downloads'] = int(''.join(downloads).split(';')[0].replace(',',''))


        item['citations'] = int(''.join(citations).split(';')[0].replace(',',''))
    

        # Authors Affectation
        item['authors_name'] = authors_name
        item['authors_university'] = authors_university
        item['authors_country'] = authors_country

        # Journal Affectation
        item['journal_name'] = publisher
        item['issn'] = issn

        # def impact_factor_of_year(year):
        #     switcher = {
        #         2013: 5.88,
        #         2014: 3.00,
        #         2015: 3.84,
        #         2016: 3.10,
        #         2017: 6.02,
        #         2018: 5.85,
        #         2019: 5.26,
        #         2020: 5.83
        #     }
        #    return switcher.get(year, 0)
        
        item['impact_factor'] = impact_factor
        item['indexation'] = indexation

        yield item

    

        
