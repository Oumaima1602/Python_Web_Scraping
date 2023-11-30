import scrapy
from articles_scraping.items import ArticlesScrapingItem
import requests


class IeeeSpider(scrapy.Spider):
    name = "ieee"
    topic = None
    #allowed_domains = ["ieeexplore.ieee.org"]
    start_urls = None
    page_no = 1
    r = None
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ieeexplore.ieee.org",
        "Content-Type": "application/json"
    }

    payload = {
        "newsearch": True,
        "queryText": topic,
        "highlight": False,
        "returnFacets": ["ALL"],
        "returnType": "SEARCH",
        "pageNumber": page_no
    }

    def __init__(self, keyword = None, topic=None, *args, **kwargs):
        super(IeeeSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://ieeexplore.ieee.org/rest/search']
        self.topic = topic
        self.payload['queryText'] = topic
        self.r = requests.post(
            "https://ieeexplore.ieee.org/rest/search",
            headers= self.headers,
            json= self.payload
        )
        

    def parse(self, response):
        item = ArticlesScrapingItem()
        
        page_data = self.r.json()
        for record in page_data["records"]:

            print(record)

            # ----------- Déclaration ----------- #
            #Article
            title = record["articleTitle"]
            topic = self.topic
            try:
                doi = record["doi"]
            except:
                doi = ""
            date_publication = record["publicationYear"]
            abstract = record["abstract"]
            references = ""
            downloads = record["downloadCount"]
            citations = record["citationCount"]

            # Authors
            authors_infos = record["authors"]
            authors_name = []
            authors_university = ""
            authors_country = ""

            l = len(authors_infos)
            for i in range(l):
                auth = authors_infos[i]
                authors_name.append(auth['preferredName'])

            # Journal
            journal_name = "IEEE"
            issn = "21682372"
            impact_factor = 3.825
            indexation = "Oui"

            # ----------- Affectation ----------- #
            # Article Affectation
            item['title'] = title
            item['topic'] = topic
            item['doi'] = doi

            try:
                item['date_publication'] = date_publication
            except:
                item['date_publication'] = 0

            item['abstract'] = abstract
            item['references'] = references
            item['downloads'] = downloads
            item['citations'] = citations
            

            # Authors Affectation
            item['authors_name'] = authors_name
            item['authors_university'] = authors_university
            item['authors_country'] = authors_country

            # Journal Affectation
            item['journal_name'] = journal_name
            item['issn'] = issn
            item['impact_factor'] = impact_factor
            item['indexation'] = indexation

        yield item


        pass
