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
    print("Start process (%s)" % time.strftime("%H:%M:%S"))
    results = get_links.get_papers_links(name)
    print("Finished extracting links (%s)" % time.strftime("%H:%M:%S"))
    print("Total amount of papers: %d" % len(results))

    user_agent = 'PRios1.1 (prios@dcc.uchile.cl)'

    # process = CrawlerProcess({
    #     'USER_AGENT': user_agent
    # })
    #
    # for result, year in results:
    #     print(result, year)
    #     process.crawl(PapersSpider(url=result, name=name, year=year),
    #                   url=result,
    #                   name=name,
    #                   year=year)
    # process.start()

    print("Finished first PDF extraction (%s)" % time.strftime("%H:%M:%S"))

    try:
        errors_path = os.getcwd() + "/pdfs/" + name + "/errors_normal.txt"
        print(errors_path)
        with open(errors_path, 'r') as f:
            reader = csv.reader(f)
            failed_results = list(reader)
    except Exception as e:
        print(e.args)
        failed_results = []

    print("Failures after normal extraction: %d" % len(failed_results))

    if len(failed_results) > 0:

        process_dynamic = CrawlerProcess({
            'USER_AGENT': user_agent
        })
        process_dynamic.crawl(PapersDynamicSpider(url=failed_results, name=name),
                              url=failed_results)
        process_dynamic.start()

    print("Finished selenium PDFs extraction (%s)" % time.strftime("%H:%M:%S"))

    try:
        errors_path = os.getcwd() + "/pdfs/" + name + "/errors_dynamic.txt"
        print(errors_path)
        with open(errors_path, 'r') as f:
            reader = csv.reader(f)
            failed_results_selenium = list(reader)
    except Exception as e:
        print(e.args)
        failed_results_selenium = []

    print("Failures after extraction with selenium: %d" % len(failed_results_selenium))


def main(argv):
    extract_papers(argv)


if __name__ == "__main__":
    main(sys.argv[1])