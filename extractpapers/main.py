from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import sys


def main(argv):
    name = str(argv)
    results = get_papers_links(name)

    ua = UserAgent()
    process = CrawlerProcess({
            'USER_AGENT': ua.random
    })

    for result in results["results"]["bindings"]:
        process.crawl(PapersSpider(url=result["homepage"]["value"],name=name),
                      url=result["homepage"]["value"],
                      name=name)
        print(result["paper"]["value"], result["homepage"]["value"])

    process.start()


def get_papers_links(name):
    sparql = SPARQLWrapper("http://dblp.l3s.de/d2r/sparql")
    sparql.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT DISTINCT ?paper ?homepage
            WHERE { ?paper foaf:maker ?maker ;
                      foaf:homepage ?homepage .
                    ?maker foaf:name '""" + name + """' .
            }
        """)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == "__main__":
   main(sys.argv[1])