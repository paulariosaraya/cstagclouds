import os
import re
from urlparse import urlparse

import scrapy
from scrapy.http import Request


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

    def start_requests(self):
        if self.url.endswith('.pdf'):
            return [Request(self.url, callback=self.save_pdf, dont_filter=True)]
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        pdf_urls = response.xpath('//a[contains(text(), "PDF") or contains(text(), "Download") or '
                                  'contains(@href, ".pdf") or contains(text(), "Download PDF")]/@href').extract()
        if len(pdf_urls) == 0:
            new_path = os.getcwd() + "/pdfs/" + self.name
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            path = new_path + "errors.txt"
            with open(path, 'a') as f:
                f.write(self.url + "\n")
        for url in pdf_urls:
            if url.startswith('/'):
                base_url = urlparse(self.url)
                with open("errors.txt", 'a') as f:
                    f.write("aaaaa" + url + "\n")
                url = '{}://{}{}'.format(base_url.scheme, base_url.netloc, url)
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