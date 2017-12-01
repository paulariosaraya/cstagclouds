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
        self.url = url

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

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