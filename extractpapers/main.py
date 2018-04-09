import sys

from scrapy.crawler import CrawlerProcess

from extractpapers.spiders.papers_spider import PapersSpider
from getlinks import get_links


def main(argv):
    name = str(argv)
    print (name)
    results = get_links.get_papers_links(name)

    user_agent = 'Prios (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    for result in results:
        process.crawl(PapersSpider(url=result,name=name),
                      url=result,
                      name=name)
        print(result)

    process.start()


if __name__ == "__main__":
    main(sys.argv[1])