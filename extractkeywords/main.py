# coding=utf-8
from __future__ import print_function

import sys

from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
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

    print(author_keywords.keywords)

    # selected = author_keywords.get_selected_keywords()
    # make_cloud(selected)

    # # Training
    # if int(is_for_training):
    #     training_output_path = '/home/paula/Descargas/Memoria/extractkeywords/training/{}.txt'.format(name)
    #     make_dir(training_output_path)
    #     training_output = open(training_output_path, "w")
    #     scores = extract_scores('/home/paula/Descargas/Memoria/extractkeywords/scores/{}.csv'.format(name))
    #     for key, keyword in top_500_keywords:
    #         keyword.set_score(scores)
    #         if keyword.score != 0:
    #             training_output.write("{},{}\n".format(keyword.to_string(),keyword.score))
    #     training_output.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
