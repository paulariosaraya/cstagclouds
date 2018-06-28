# coding=utf-8
from __future__ import print_function

import sys

import os

from extractkeywords.utils import extract_scores, make_dir
from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
from extractkeywords.features.tfidf import TfidfCalculator
from extractkeywords.features.wiki_url import Searcher
from tagclouds.make_cloud import make_cloud


def main(name, needs_convert, is_filtered):
    name = str(name).replace(' ', '_')
    needs_convert = int(needs_convert)
    # Convert pdf to txt if needed
    if needs_convert:
        path = '/home/paula/Descargas/Memoria/extractpapers/pdfs/{}/'.format(name)
        txt_path = convert_all(path)
    else:
        txt_path = '/home/paula/Descargas/Memoria/extractkeywords/txt/{}/'.format(name)

    # Get ranked keywords from all the papers
    author_keywords = AuthorKeywords(txt_path, name, is_filtered)
    author_keywords.extract_keywords()

    
    # [print(e[0], e[1].rake_score) for e in author_keywords.keywords]
    if is_filtered:
        filter = "filtered"
    else:
        filter = "unfiltered"
    models = ["LinearRegression", "RankSVM", "LambdaMART", "AdaRank"]
    for model_name in models:
        model_path_author = "/home/paula/Descargas/Memoria/learningtorank/models/%s/%s/%s_model_%s.sav" % (filter, model_name, model_name[0].lower() + model_name[1:], name)
        if os.path.exists(model_path_author):
            model_path = model_path_author
        else:
            model_path = "/home/paula/Descargas/Memoria/learningtorank/models/%s/%s_model.sav" % (filter, model_name[0].lower() + model_name[1:])

        selected = author_keywords.get_selected_keywords(model_path)
        make_cloud(selected, model_name, name, filter)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
