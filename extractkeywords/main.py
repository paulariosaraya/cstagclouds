# coding=utf-8
from __future__ import print_function

import sys

from extractkeywords.utils import extract_scores, make_dir
from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
from extractkeywords.features.tfidf import TfidfCalculator
from extractkeywords.features.wiki_url import Searcher
from tagclouds.make_cloud import make_cloud


def main(name, needs_convert, is_for_training):
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

    selected = author_keywords.get_selected_keywords()
    make_cloud(selected)

    # Training
    if int(is_for_training):
        training_output_path = '/home/paula/Descargas/Memoria/extractkeywords/training/{}.txt'.format(name)
        make_dir(training_output_path)
        training_output = open(training_output_path, "w")
        scores = extract_scores('/home/paula/Descargas/Memoria/extractkeywords/scores/{}.csv'.format(name))
        # Wiki searcher
        bin_searcher = Searcher('/features/enwiki-latest-all-titles-in-ns0')
        # Tfidf cal
        tfidf_calc = TfidfCalculator("/home/paula/Descargas/Memoria/extractkeywords/txt/*/",
                                     [element[0] for element in author_keywords.keywords])
        tfidf = tfidf_calc.get_tfidf_feats(name)
        for key, keyword in author_keywords.keywords:
            keyword.set_score(scores)
            keyword.set_is_in_wiki(1 if bin_searcher.find(key.replace(' ', '_')) else 0)
            keyword.set_tfidf(tfidf[key])
            if keyword.score != 0:
                training_output.write("{},{}\n".format(keyword.to_string(),keyword.score))
        training_output.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
