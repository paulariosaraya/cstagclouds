import scrapy
import time
from scrapy.http import Request
import os
import re


class PapersSpider(scrapy.Spider):
    name = "papers"

    def __init__(self, *args, **kwargs):
        super(PapersSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('url')
        if not url:
            raise ValueError('No url given')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        if url.startswith('http://dx.doi.org/doi.org%'):
            url = re.sub(r'doi.org(?=%)', '', url)
        self.url = url

        self.name = kwargs.get('name').replace(" ", "_") + "/"
        if kwargs.get('wait'):
            time.sleep(5)

    def start_requests(self):
        if self.url.endswith('.pdf'):
            return [Request(self.url, callback=self.save_pdf, dont_filter=True)]
        Request(self.url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        pdf_urls = response.xpath('//a[contains(text(), "PDF") or contains(text(), "Download") or '
                                  'contains(@href, ".pdf") or contains(text(), "Download PDF")]/@href').extract()
        if len(pdf_urls) == 0:
            file = open("errors.txt", 'a')
            file.write(self.url + "\n")
            file.close()
        for url in pdf_urls:
            yield Request(
                url=response.urljoin(url),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        new_path = os.getcwd()+"/pdfs/"+self.name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        path = new_path+response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)