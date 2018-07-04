import os
import re

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request


class PapersSpider(scrapy.Spider):
    name = "papers"
    custom_settings = {
        'DOWNLOAD_MAXSIZE': 7340032,
    }

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
        self.year = kwargs.get('year')

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
            path = new_path + "errors_normal.txt"
            with open(path, 'a') as f:
                f.write("%s, %s\n" % (self.url, self.year))
        else:
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
        if len(path.split('.pdf')) > 1:
            path = "{}_{}.pdf".format(path.split('.pdf')[0], self.year)
        else:
            path = "{}_{}".format(path, self.year)
        with open(path, 'wb') as f:
            f.write(response.body)