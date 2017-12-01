from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess

spider = PapersSpider(domain='https://dl.acm.org/citation.cfm?doid=1242572.1242819')
process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(spider)
process.start()