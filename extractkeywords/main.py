# coding=utf-8
from __future__ import print_function

import sys

from extractkeywords.utils import extract_scores, make_dir
from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
from extractkeywords.features.tfidf import TfidfCalculator
from extractkeywords.features.wiki_url import Searcher
from tagclouds.make_cloud import make_cloud


def main(name, needs_convert):
    name = str(name).replace(' ', '_')
    needs_convert = int(needs_convert)
    # Convert pdf to txt if needed
    if needs_convert:
        path = '/home/paula/Descargas/Memoria/extractpapers/pdfs/{}/'.format(name)
        txt_path = convert_all(path)
    else:
        txt_path = '/home/paula/Descargas/Memoria/extractkeywords/txt/{}/'.format(name)

    # Get ranked keywords from all the papers
    author_keywords = AuthorKeywords(txt_path, name)
    author_keywords.extract_keywords()

    # [print(e[0], e[1].rake_score) for e in author_keywords.keywords]

    selected = author_keywords.get_selected_keywords('/home/paula/Descargas/Memoria/learningtorank/rank_SVM_model.sav')
    make_cloud(selected)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
