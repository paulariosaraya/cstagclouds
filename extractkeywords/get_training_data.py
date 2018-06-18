# coding=utf-8
from __future__ import print_function

import glob

from extractkeywords.utils import extract_scores, make_dir
from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.features.tfidf import TfidfCalculator
from extractkeywords.features.wiki_url import Searcher


def main():
    scores_dir = '/home/paula/Descargas/Memoria/extractkeywords/scores/*.csv'
    for filename in glob.glob(scores_dir):
        name = filename.split('/')[-1].replace('.csv', '')
        txt_path = '/home/paula/Descargas/Memoria/extractkeywords/txt/{}/'.format(name)

        # Get ranked keywords from all the papers
        author_keywords = AuthorKeywords(txt_path, name)
        author_keywords.extract_keywords()

        training_output_path = '/home/paula/Descargas/Memoria/extractkeywords/training/{}.txt'.format(name)
        make_dir(training_output_path)
        training_output = open(training_output_path, "w")
        scores = extract_scores('/home/paula/Descargas/Memoria/extractkeywords/scores/{}.csv'.format(name))
        # Wiki searcher
        bin_searcher = Searcher('/home/paula/Descargas/Memoria/extractkeywords/features/enwiki-latest-all-titles-in-ns0')
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
    main()
