# coding=utf-8
from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess


def main():
    name = "s"
    user_agent = 'Prios (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    url = 'https://dl.acm.org/citation.cfm?doid=3077136.3096474'

    process.crawl(PapersSpider(url=url, name=name),
                  url=url,
                  name=name)
    print(url)

    process.start()


if __name__ == "__main__":
    main()