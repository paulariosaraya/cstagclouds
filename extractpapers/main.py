import csv
import sys

import time

import os
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider

from extractpapers.getlinks import get_links
from extractpapers.paperspiders.spiders.papers_dynamic_spider import PapersDynamicSpider
from extractpapers.paperspiders.spiders.papers_spider import PapersSpider


def extract_papers(url):
    name = str(url).split('/')[-1]
    print(name)
    results = get_links.get_papers_links(name)

    user_agent = 'PRios1.1 (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    for result, year in results:
        print(result, year)
        process.crawl(PapersSpider(url=result, name=name, year=year),
                      url=result,
                      name=name,
                      year=year)
    process.start()
    #
    # try:
    #     errors_path = os.getcwd() + "/pdfs/" + name + "/errors_normal.txt"
    #     print(errors_path)
    #     with open(errors_path, 'r') as f:
    #         reader = csv.reader(f)
    #         failed_results = list(reader)
    # except Exception as e:
    #     print(e.args)
    #     failed_results = []
    #
    # print(failed_results)
    #
    # if len(failed_results) > 0:
    #     # process_dynamic = CrawlerProcess({
    #     #     'USER_AGENT': user_agent
    #     # })
    #     for result, year in failed_results:
    #         print(result, year)
    #         process_dynamic = CrawlerProcess({
    #             'USER_AGENT': user_agent
    #         })
    #         process_dynamic.crawl(PapersDynamicSpider(url=result, name=name, year=year),
    #                       url=result,
    #                       name=name,
    #                       year=year)
    #         process_dynamic.start()
    #     # process_dynamic.start()


def main(argv):
    extract_papers(argv)


if __name__ == "__main__":
    main(sys.argv[1])