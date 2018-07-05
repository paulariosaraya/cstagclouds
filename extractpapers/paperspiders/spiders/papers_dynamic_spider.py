import os
import re

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait


class PapersDynamicSpider(scrapy.Spider):
    name = "papers_dynamic"
    custom_settings = {
        'DOWNLOAD_MAXSIZE': 7340032,
    }

    def __init__(self, *args, **kwargs):
        super(PapersDynamicSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('url')
        if not url:
            raise ValueError('No url given')
        self.url = url

        self.name = kwargs.get('name')
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def start_requests(self):
        for url, year in self.url:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://%s/' % url
            if url.startswith('http://dx.doi.org/doi.org%'):
                url = re.sub(r'doi.org(?=%)', '', url)
            url.replace(" ", "_") + "/"
            if url.endswith('.pdf'):
                request = Request(url, callback=self.save_pdf)
            else:
                request = Request(url, callback=self.parse)
            request.meta['year'] = year
            yield request

    def parse(self, response):
        year = response.meta['year']
        # selenium part of the job
        self.driver.get(response.url)
        try:
            cookies = WebDriverWait(self.driver, 20).until(
                element_to_be_clickable((By.XPATH, '//a[contains(., "Close")]')))
            cookies.click()
        except TimeoutException:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    element_to_be_clickable((By.XPATH, '//a[contains(., "PDF") or contains(., "Download")]')))
                element.click()
                url = self.driver.find_element_by_xpath('//iframe')
                request = Request(
                    url=response.urljoin(url.get_attribute("src")),
                    callback=self.save_pdf
                )
                request.meta['year'] = year
                yield request
            except TimeoutException:
                print("os", os.getcwd() is None)
                print("name", self.name is None)
                new_path = os.getcwd() + "/pdfs/" + "test2"
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                path = new_path + "errors_dynamic.txt"
                with open(path, 'a') as f:
                    f.write(self.url + "\n")
                self.driver.close()

    def save_pdf(self, response):
        year = response.meta['year']
        new_path = os.getcwd() + "/pdfs/" + "test2"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        path = new_path + response.url.split('/')[-1]
        if len(path.split('.pdf')) > 1:
            path = "{}_{}.pdf".format(path.split('.pdf')[0], year)
        else:
            path = "{}_{}".format(path, year)
        with open(path, 'wb') as f:
            f.write(response.body)