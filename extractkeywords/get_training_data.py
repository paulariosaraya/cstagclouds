# coding=utf-8
from __future__ import print_function

import glob
import os

from cstagclouds.extractkeywords.author_keywords import AuthorKeywords
from cstagclouds.extractkeywords.utils import extract_scores, make_dir

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def main():

    scores_dir = os.path.join(__location__, 'scores/*.csv')
    for filename in glob.glob(scores_dir):
        name = filename.split('/')[-1].replace('.csv', '')
        txt_path = os.path.join(__location__, 'txt/{}/'.format(name))

        # Get ranked keywords from all the papers
        author_keywords = AuthorKeywords(txt_path, name, 0)
        author_keywords.extract_keywords()

        training_output_path = os.path.join(__location__, 'training/{}.txt'.format(name))
        make_dir(training_output_path)
        training_output = open(training_output_path, "w")
        scores = extract_scores(os.path.join(__location__, 'scores/{}.csv'.format(name)))
        for key, keyword in author_keywords.keywords:
            keyword.set_score(scores)
            if keyword.score != 0:
                training_output.write("{},{}\n".format(keyword.to_string(),keyword.score))
        training_output.close()


if __name__ == "__main__":
    main()
