import scrapy
from scrapy.http import Request
from extractpapers.items import ExtractpapersItem


class PapersSpider(scrapy.Spider):
    name = "papers"

    def __init__(self, *args, **kwargs):
        #super(PapersSpider, self).__init__(**kw)
        #url = kw.get('url')
        #if not url:
        #    raise ValueError('No url given')
        #if not url.startswith('http://') and not url.startswith('https://'):
        #    url = 'http://%s/' % url*

        super(PapersSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('url')
        if not url:
            raise ValueError('No url given')
        self.url = url
        #self.url = "https://jbiomedsem.biomedcentral.com/articles/10.1186/s13326-017-0112-6"


    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

        #
        #urls = [
        #    'https://jbiomedsem.biomedcentral.com/articles/10.1186/s13326-017-0112-6'
        #]
        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse)
        #

    def parse(self, response):
        pdf_urls = response.xpath('//a[contains(text(), "PDF")]/@href').extract()
        for url in pdf_urls:
            yield Request(
                url=response.urljoin(url),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)