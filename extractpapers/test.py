# -*- coding: utf-8 -*-
import sys
from namedentities import *


def main(argv):
    get_papers_links(argv)

def get_papers_links(raw_name):
    user_page = get_user_page(raw_name)
    # Download the file
    # get papers links


def get_user_page(raw_name):
    # Formatting name
    name = raw_name.decode('utf-8')
    name = ' '.join(word[0].upper() + word[1:] for word in name.split())
    name = repr(named_entities(name)).replace(';', '=').replace('&', '=').replace("'", "")
    first, last = name.split(' ')
    name = last + ":" + first
    # Getting surname initial
    initial = name[0].lower()
    return "http://dblp.org/pers/%s/%s.nt" % (initial, name)


if __name__ == "__main__":
   main(sys.argv[1])