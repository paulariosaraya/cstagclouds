import os
import re

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from selenium import webdriver


class PapersDynamicSpider(scrapy.Spider):
    name = "papers_dynamic"

    def __init__(self, *args, **kwargs):
        super(PapersDynamicSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('url')
        if not url:
            raise ValueError('No url given')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        if url.startswith('http://dx.doi.org/doi.org%'):
            url = re.sub(r'doi.org(?=%)', '', url)
        self.url = url

        self.name = kwargs.get('name').replace(" ", "_") + "/"
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def start_requests(self):
        if self.url.endswith('.pdf'):
            return [Request(self.url, callback=self.save_pdf, dont_filter=True)]
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        # selenium part of the job
        self.driver.get(response.url)
        link = self.driver.find_element_by_xpath('//a[contains(., "PDF") or contains(., "Download")]')
        link.click()
        #while True:
        #    # response.xpath('//button[contains(., "Download")]/@href').extract()
        #    link = self.driver.find_element_by_xpath('//a[contains(text(), "PDF") or contains(text(), "Download")/@href')

        #    try:
        #        next.click()

                # get the data and write it to scrapy items
        #    except:
        #        break

        #pdf_urls = response.xpath('//a[contains(text(), "PDF") or contains(text(), "Download") or '
        #                          'contains(@href, ".pdf") or contains(text(), "Download PDF")]/@href').extract()

        url = self.driver.find_element_by_xpath('//iframe')
        yield Request(
            url=response.urljoin(url.get_attribute("src")),
            callback=self.save_pdf
        )

    def save_pdf(self, response):
        new_path = os.getcwd()+"/pdfs/"+self.name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        path = new_path+response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)