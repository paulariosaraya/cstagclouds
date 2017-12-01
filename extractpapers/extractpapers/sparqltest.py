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
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["paper"]["value"], result["homepage"]["value"])