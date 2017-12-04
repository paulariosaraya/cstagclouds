from extractpapers.spiders.papers_spider import PapersSpider
from scrapy.crawler import CrawlerProcess

from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("http://dblp.l3s.de/d2r/sparql")
sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT DISTINCT ?paper ?homepage
    WHERE { ?paper foaf:maker ?maker ;
              foaf:homepage ?homepage .
            ?maker foaf:name "Aidan Hogan" .
    }
    LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

for result in results["results"]["bindings"]:
    process.crawl(PapersSpider(url=result["homepage"]["value"]),url=result["homepage"]["value"])
    print(result["paper"]["value"], result["homepage"]["value"])

process.start()