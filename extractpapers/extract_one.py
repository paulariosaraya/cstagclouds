# coding=utf-8
from scrapy.crawler import CrawlerProcess

from extractpapers.paperspiders.spiders.papers_dynamic_spider import PapersDynamicSpider
from extractpapers.paperspiders.spiders.papers_spider import PapersSpider


def main():
    name = "test"
    user_agent = 'Prios (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    url = 'https://doi.org/10.1109/LA-WEB.2012.11'

    process.crawl(PapersSpider(url=url, name=name),
                  url=url,
                  name=name,
                  year=2012)
    print(url)

    process.start()


if __name__ == "__main__":
    main()