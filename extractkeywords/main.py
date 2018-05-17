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

# classifier: define features
# of tf idf? some
# anyway we would need features
# basis from tf idf, score from rake, does the keyword appear in wikipedia? (to see if it's too specific)
# how to do this (api, or list of urls from wikipedia)

# year it was published first and latest

# number/ratio of docs the keyword was included [done]

# phrase depth 1 - prob(word appearing)
# 1 - (first ap / word count)
# position in document 1/1 if it's in the begining 1/x if it's at the x position
# (sum all the weights if it appears many times)
# maybe  1/log(x)?
# or another metric
# w-p/w w=amount of words, p=position
# w/p inverted probability of word being in the top p positions
# 1/p to consider document length

# model needs to be able to consider ordinal classes

# Related work keywords extraction techniques, (topic modelling latent dirichlet allocarion), DM(ML)  the metrics, tag clouds
# Proposed solution 4 things: architecture, accesing dblp, downloading pdfs, extraction,
# keywords extraction, features (and why?), model, tag cloud creation final system
# Evaluation: initial training set (what we just did), evaluation and training presition and measures of evaluation
# Conclusion: summary, real conclusions why it worked, future work

# finish a week before deadline!!!

# try to remove hyphen and see if it exists in the set
# if it is keep it, if not replace it with a space.

# Define how many keywords should be in the tag clouds
# try to find a reference or define a reasonable number
# or just try


# Filter by frequency until classes are balanced?
# Using term frequency across all papers
# Continue until 1 isn't the class with the most elements?
# We don't want to lose 3s 4s and 5s..


# Try 10 fold cross validation

# See if any of the models produce a score or something to define the size of the text