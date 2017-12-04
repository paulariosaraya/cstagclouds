import scrapy
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

    def start_requests(self):
        if self.url.endswith('.pdf'):
            return [Request(self.url, callback=self.save_pdf, dont_filter=True)]
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        pdf_urls = response.xpath('//a[contains(text(), "PDF") or contains(text(), "Download") or contains(text(), "Download PDF")]/@href').extract()
        for url in pdf_urls:
            yield Request(
                url=response.urljoin(url),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        newpath = os.getcwd()+"/pdfs/"+self.name
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        path = newpath+response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)