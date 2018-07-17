import csv
import os
import sys
import time

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from cstagclouds.extractpapers.getlinks import get_links
from cstagclouds.extractpapers.paperspiders.spiders.papers_dynamic_spider import PapersDynamicSpider
from cstagclouds.extractpapers.paperspiders.spiders.papers_spider import PapersSpider


def extract_papers(name):
    results = get_links.get_papers_links(name)
    print("Finished extracting links (%s)" % time.strftime("%H:%M:%S"))
    print("Total amount of papers: %d" % len(results))

    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        for result, year in results:
            print(result, year)
            yield runner.crawl(PapersSpider(url=result, name=name, year=year),
                               url=result,
                               name=name,
                               year=year)
        failed_downloads = get_failures(name)
        recall = (len(results) - len(failed_downloads)) / len(results)
        print("Finished downloading papers (%s)" % time.strftime("%H:%M:%S"))
        print("recall = %f" % recall)
        if recall < 0.6:
            yield runner.crawl(PapersDynamicSpider(url=failed_downloads, name=name),
                               url=failed_downloads,
                               name=name)
        reactor.stop()

    crawl()
    reactor.run()


def get_failures(name):
    try:
        errors_path = os.getcwd() + "/pdfs/" + name + "/errors_normal.txt"
        print(errors_path)
        with open(errors_path, 'r') as f:
            reader = csv.reader(f)
            failed_results = list(reader)
    except Exception as e:
        print(e.args)
        failed_results = []
    return failed_results


def extract_dynamic(name, failed_downloads=None):
    user_agent = 'PRios1.1 (prios@dcc.uchile.cl)'

    if failed_downloads is None:
        failed_downloads = get_failures(name)

    print("Failures after normal extraction: %d" % len(failed_downloads))

    process_dynamic = CrawlerProcess({
        'USER_AGENT': user_agent
    })
    process_dynamic.crawl(PapersDynamicSpider(url=failed_downloads, name=name),
                          url=failed_downloads,
                          name=name)
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


def main(url):
    print("Start process (%s)" % time.strftime("%H:%M:%S"))
    name = str(url).split('/')[-1]
    extract_papers(name)


if __name__ == "__main__":
    main(sys.argv[1])