from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from getlinks import get_links
import sys


def main(argv):
    name = str(argv)
    print name
    results = get_links.get_papers_links(name)

    ua = UserAgent()
    process = CrawlerProcess({
            'USER_AGENT': ua.random
    })

    for result in results:
        process.crawl(PapersSpider(url=result,name=name),
                      url=result,
                      name=name)
        print(result)

    process.start()


if __name__ == "__main__":
    main(sys.argv[1])