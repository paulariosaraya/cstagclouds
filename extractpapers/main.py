from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from getlinks import get_links
import sys


def main(argv):
    name = str(argv)
    print (name)
    results = get_links.get_papers_links(name)

    process = CrawlerProcess()

    for result in results:
        answer = process.crawl(PapersSpider(url=result,name=name,wait=False),
                      url=result,
                      name=name)
        if answer == False:
            answer = process.crawl(PapersSpider(url=result, name=name, wait=True),
                       url=result,
                       name=name)
        print(result)

    process.start()


if __name__ == "__main__":
    main(sys.argv[1])