import sys

from extractpapers.spiders.papers_dynamic_spider import PapersDynamicSpider
from extractpapers.spiders.papers_spider import PapersSpider
from getlinks import get_links
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider


def main(argv):
    name = str(argv).split('/')[-1]
    print (name)
    results = get_links.get_papers_links(name)

    user_agent = 'PRios1.1 (prios@dcc.uchile.cl)'

    process = CrawlerProcess({
        'USER_AGENT': user_agent
    })

    for result, year in results:
        print(result, year)
        try:
            process.crawl(PapersSpider(url=result,name=name,year=year),
                          url=result,
                          name=name,
                          year=year)
        except CloseSpider:
            process.crawl(PapersDynamicSpider(url=result, name=name,year=year),
                          url=result,
                          name=name,
                          year=year)
    process.start()


if __name__ == "__main__":
    main(sys.argv[1])