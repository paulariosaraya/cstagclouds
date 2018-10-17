# -*- coding: utf-8 -*-
import re

import rdflib
from rdflib import URIRef


def get_papers_links(raw_name):
    paper_links = []
    user_page = get_user_page(raw_name)
    g = rdflib.Graph()
    g.load(user_page, format="nt")
    # Predicates
    author_of = URIRef("https://dblp.org/rdf/schema-2017-04-18#authorOf")
    electronic_edition = URIRef("https://dblp.org/rdf/schema-2017-04-18#primaryElectronicEdition")
    year_of_publication = URIRef("https://dblp.org/rdf/schema-2017-04-18#yearOfPublication")
    for o in g.objects(predicate=author_of):
        g_paper = rdflib.Graph()
        g_paper.load(o + ".nt", format="nt")
        try:
            paper_homepage = list(g_paper.objects(predicate=electronic_edition))[0]
            paper_year = list(g_paper.objects(predicate=year_of_publication))[0]
            paper_links.append([paper_homepage, paper_year])
        except IndexError:
            pass
    return paper_links


def get_user_page(raw_name):
    name = raw_name
    initial = name[0].lower()
    return "https://dblp.org/pers/%s/%s.nt" % (initial, name)
