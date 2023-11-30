from typing import Any, Optional
import scrapy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from articles_scraping.items import ArticlesScrapingItem
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager



class SciencedirectSpider(scrapy.Spider):
    name = "sciencedirect"
    start_urls = None
    chrome_options = Options()
    #driver = webdriver.Chrome(executable_path = os.path.abspath("D:/Downloads_2023_2024/chromedriver_win32/chromedriver.exe"),options=chrome_options)
    
    def __init__(self, topic = None, *args, **kwargs):
        super(SciencedirectSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.sciencedirect.com/search?qs=" + topic]
        self.topic = topic
        #self.driver.get("https://www.sciencedirect.com/search?qs=" + topic)
   
    def start_requests(self):
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={'driver': driver, 'topic': self.topic})

    
    def parse(self, response):
        delay = 10
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'srp-results-list')))
            elements = self.driver.find_elements(By.CSS_SELECTOR,"div.result-item-content h2 span a")
            for element in elements:
                article = element.get_attribute("href")
                driver1 = webdriver.Chrome(executable_path = os.path \
                                           .abspath("D:/Downloads_2023_2024/chromedriver_win32/chromedriver.exe"), options=self.chrome_options)
                driver1.get(str(article))

            # ----------- Déclaration ----------- #
            # Authors
            authors_name = []
            authors_infos = []
            authors_university = []
            authors_country = []

            # Article
            title = ""
            topic = ""
            doi = ""
            date_publication = 0
            abstract = ""
            references = []
            citations = 0
            downloads = 0
            try:
                Elem = WebDriverWait(driver1, delay).until(EC.presence_of_element_located((By.ID, 'abstracts')))
                elements1 = driver1.find_elements(By.CSS_SELECTOR, "span.title-text")
                for element1 in elements1:
                    title = element1.text
                elements1 = driver1.find_elements(By.CSS_SELECTOR,
                                                  "div#author-group.author-group a.author.size-m.workspace-trigger span.content")
                for element1 in elements1:
                    authors_name.append(element1.text)

                #authors_infos
                elems = driver1.find_elements(By.CSS_SELECTOR,"button#show-more-btn")
                ActionChains(driver1).click(elems[0]).perform()
                elements1 = driver1.find_elements(By.CSS_SELECTOR, "dl.affiliation dd")
                for element1 in elements1:
                    authors_infos.append(element1.text)

                elements1 = driver1.find_elements(By.CSS_SELECTOR, "a.doi")
                for element1 in elements1:
                    doi = element1.text
                elements1 = driver1.find_elements(By.CSS_SELECTOR, "div#publication.Publication div.publication-volume div.text-xs")
                for element1 in elements1:
                    date_publication = element1.text
                elements1 = driver1.find_elements(By.CSS_SELECTOR, "div#abstracts.Abstracts.u-font-serif")
                for element1 in elements1:
                    abstract = element1.text
                elements1 = driver1.find_elements(By.CSS_SELECTOR, "ul li.bib-reference.u-margin-s-bottom")
                for element1 in elements1:
                    references.append(element1.text)

            except TimeoutException:
                print("Loading took too much time!")
            driver1.quit()

            item = ArticlesScrapingItem()

            item['title'] = title
            item['abstract'] = abstract
            item['authors_name'] = authors_name
            item['topic'] = topic
            item['doi'] = doi
            item['date_publication'] = date_publication
            item['journal_name'] = "ScienceDirect"
            item['downloads'] = downloads
            item['references'] = references

            yield item
        except TimeoutException:
            print("Loading took too much time!")
        self.driver.quit()


        pass
