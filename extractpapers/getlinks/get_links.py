# -*- coding: utf-8 -*-
import re

import rdflib
from rdflib import URIRef


def get_papers_links(raw_name):
    paper_links = []

    user_page = get_user_page(raw_name)
    print(user_page)
    g = rdflib.Graph()
    g.load(user_page)
    author_of = URIRef("https://dblp.org/rdf/schema-2017-04-18#authorOf")
    electronic_edition = URIRef("https://dblp.org/rdf/schema-2017-04-18#primaryElectronicEdition")
    year_of_publication = URIRef("https://dblp.org/rdf/schema-2017-04-18#yearOfPublication")
    for o in g.objects(predicate=author_of):
        g_paper = rdflib.Graph()
        g_paper.load(o + ".rdf")
        paper_homepage = list(g_paper.objects(predicate=electronic_edition))[0]
        paper_year = list(g_paper.objects(predicate=year_of_publication))[0]
        print(paper_homepage, paper_year)
        paper_links.append([paper_homepage, paper_year])
    #
    # # Download rdf file
    # r = requests.get(user_page, allow_redirects=True)
    # open(user_page.split("/")[-1], 'wb').write(r.content)
    #
    # paper_links = []
    #
    # # Get every link to paper rdf files
    # author_file = open(user_page.split("/")[-1], 'r')
    # for line in author_file:
    #     split_line = line.split("#authorOf")
    #     if len(split_line) > 1:
    #         # Format url
    #         paper_page = get_paper_page(split_line[1])
    #
    #         # Download rdf file
    #         paper_page_path = paper_page.split("/")[-1]
    #         r = requests.get(paper_page, allow_redirects=True)
    #         open(paper_page_path, 'wb').write(r.content)
    #
    #         # Get link to electronic edition of paper
    #         paper_file = open(paper_page_path, 'r')
    #         for line2 in paper_file:
    #             if "#primaryElectronicEdition" in line2:
    #                 paper_homepage = line2.split("#primaryElectronicEdition> <")[1]
    #                 paper_homepage = paper_homepage.split('>')[0]
    #             if "#yearOfPublication" in line2:
    #                 paper_year = line2.split("#yearOfPublication> \"")[1]
    #                 paper_year = paper_year.split('"')[0]
    #         paper_links.append([paper_homepage, paper_year])
    #         # Close file
    #         paper_file.close()
    #         os.remove(paper_page_path)

    # author_file.close()
    return paper_links


def get_user_page(raw_name):
    # Formatting name
    #name = raw_name
    #name = ' '.join(word[0].upper() + word[1:] for word in name.split())
    #name = re.sub(r'[;.&]', "=",repr(named_entities(name)).replace("'", ""))
    #print(name)
    #names = name.split(' ')
    #last =
    #if len(names) > 2:
    #    first = names[0:-1].join('_')
    #name = last + ":" + first
    # Getting surname initial
    name = raw_name
    initial = name[0].lower()
    return "https://dblp.org/pers/%s/%s.rdf" % (initial, name)


def get_paper_page(line):
    paper_page = line.split('dblp.org/rec/')[1]
    paper_page = re.sub(r'[>\s*.]', '', paper_page)
    paper_page = "https://dblp.uni-trier.de/rec/nt/%s.nt" % paper_page
    return paper_page
