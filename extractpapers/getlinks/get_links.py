# -*- coding: utf-8 -*-
import sys
import re
import os
import requests
from namedentities import *

def get_papers_links(raw_name):
    user_page = get_user_page(raw_name)

    # Download rdf file
    r = requests.get(user_page, allow_redirects=True)
    open(user_page.split("/")[-1], 'wb').write(r.content)

    paper_links = []

    # Get every link to paper rdf files
    author_file = open(user_page.split("/")[-1], 'r')
    for line in author_file:
        split_line = line.split("#authorOf")
        if len(split_line) > 1:
            # Format url
            paper_page = get_paper_page(split_line[1])

            # Download rdf file
            paper_page_path = paper_page.split("/")[-1]
            r = requests.get(paper_page, allow_redirects=True)
            open(paper_page_path, 'wb').write(r.content)

            # Get link to electronic edition of paper
            paper_file = open(paper_page_path, 'r')
            for line2 in paper_file:
                if "#primaryElectronicEdition" in line2:
                    paper_homepage = line2.split("#primaryElectronicEdition> <")[1]
                    paper_homepage = paper_homepage.split('>')[0]
                    paper_links.append(paper_homepage)

            # Close file
            paper_file.close()
            os.remove(paper_page_path)

    author_file.close()
    return paper_links


def get_user_page(raw_name):
    # Formatting name
    name = raw_name.decode('utf-8')
    name = ' '.join(word[0].upper() + word[1:] for word in name.split())
    name = repr(named_entities(name)).replace(';', '=').replace('&', '=').replace("'", "")
    first, last = name.split(' ')
    name = last + ":" + first
    # Getting surname initial
    initial = name[0].lower()
    return "https://dblp.org/pers/%s/%s.nt" % (initial, name)


def get_paper_page(line):
    paper_page = line.split('dblp.org/rec/')[1]
    paper_page = re.sub(r'[>\s*.]', '', paper_page)
    paper_page = "https://dblp.uni-trier.de/rec/nt/%s.nt" % paper_page
    return paper_page