# coding=utf-8
from extractpapers.spiders.papers_dynamic_spider import PapersDynamicSpider
from scrapy.crawler import CrawlerProcess
import os


def main():
    name = "test"
    user_agent = 'Prios (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    url = 'https://doi.org/10.1109/ISM.2016.0106'

    process.crawl(PapersDynamicSpider(url=url, name=name),
                  url=url,
                  name=name)
    print(url)

    process.start()


if __name__ == "__main__":
    main()