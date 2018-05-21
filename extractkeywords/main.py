# coding=utf-8
from __future__ import print_function

import datetime
import sys

from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.tfidf import TfidfCalculator
from extractkeywords.wiki_url import Searcher
from extractkeywords.parser import convert_all, make_dir
from extractkeywords.add_score import extract_scores


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
    ranked_keywords = author_keywords.get_keywords()

    # Write to file
    output_path_top500 = '/home/paula/Descargas/Memoria/extractkeywords/keywords/{}/{}_500.txt'.format(name, str(datetime.datetime.now()))
    make_dir(output_path_top500)
    output_file_top500 = open(output_path_top500, "w")  # make text file

    # Top 500
    top_500_keywords = list(ranked_keywords[0:500])
    # shuffle(top_500_keywords)

    # Wiki searcher
    bin_searcher = Searcher('enwiki-latest-all-titles-in-ns0')

    # Tfidf cal
    tfidf_calc = TfidfCalculator("/home/paula/Descargas/Memoria/extractkeywords/txt/*/",
                                 [element[0] for element in top_500_keywords])
    tfidf = tfidf_calc.get_tfidf_feats(name)

    for key, keyword in top_500_keywords:
        keyword.set_is_in_wiki(1 if bin_searcher.find(key.replace(' ', '_')) else 0)
        keyword.set_tfidf(tfidf[key])
        output_file_top500.write("{}\n".format(keyword.to_string()))
    output_file_top500.close()

    # Training
    training_output_path = '/home/paula/Descargas/Memoria/extractkeywords/training/{}.txt'.format(name)
    make_dir(training_output_path)
    training_output = open(training_output_path, "w")
    scores = extract_scores('/home/paula/Descargas/Memoria/extractkeywords/scores/{}.csv'.format(name))
    for key, keyword in top_500_keywords:
        keyword.set_score(scores)
        if keyword.score != 0:
            training_output.write("{},{}\n".format(keyword.to_string(),keyword.score))
    training_output.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
