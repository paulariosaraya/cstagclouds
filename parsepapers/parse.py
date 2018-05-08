# coding=utf-8
from __future__ import print_function

import datetime
import glob
import os
import re
import sys

from collections import Counter
from io import BytesIO
from random import shuffle

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

from parsepapers import rake

from parsepapers.wiki_url import Searcher
from parsepapers.tfidf import TfidfCalculator


def is_binary(filename):
    f = os.popen('file -bi '+filename, 'r')
    file_type = f.read()
    if file_type.startswith('text') or file_type.startswith('image'):
        print(file_type)
        return False
    else:
        return True


def make_dir(filename):
    new_path = os.path.split(filename)[0]
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def write_text(text, text_filename):
    make_dir(text_filename)
    with open(text_filename, 'w') as f:
        f.write(text)


def clean(text):
    text = text.decode('utf-8')
    text = re.sub(r'(\w+)(-\s+)(\w+(\s|[,;.]))', r'\1\3\n', text, flags=re.MULTILINE)
    return text


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    num_pages = 0
    for page in PDFPage.get_pages(infile, pagenums):
        if num_pages > 60:
            raise Exception('Page limit')
        interpreter.process_page(page)
        num_pages += 1
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def convert_all(path):
    path_base = "{}/txt/{}".format(os.path.dirname(os.path.realpath(__file__)), path.split("/")[-2])
    for filename in glob.glob(os.path.join(path, '*')):
        path_split = os.path.split(filename)
        text_filename = "{}/{}.txt".format(path_base, path_split[1])
        if is_binary(filename) and not os.path.exists(text_filename):
            print(text_filename)
            try:
                text = convert(filename)
                text = clean(text)
                write_text(text, text_filename)
            except PDFSyntaxError:
                print(filename)
            except Exception:
                print(filename)

    return path_base


def get_ranked_keywords(result, n):
    score_counter = Counter()
    ratio_counter = Counter()
    years = {}
    for keywords, year in result:
        for keyword in keywords:
            score_counter[keyword[0]] += keyword[1]
            ratio_counter[keyword[0]] += 1 / n
            years.setdefault(keyword[0],[]).append(year)
    latest_years = {k: max(years[k]) for k in years}
    first_years = {k: min(years[k]) for k in years}
    dict = {key: [score_counter[key], ratio_counter[key], first_years[key], latest_years[key]] for key in score_counter}
    return sorted(dict.items(), key=lambda x: x[1][0], reverse=True)


def get_all_keywords(txt_path):
    result = []
    rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 3)
    papers_count = 0
    for filename in glob.glob(os.path.join(txt_path, '*.txt')):
        with open(filename, 'r') as paper_file:
            text = paper_file.read()
            result.append([rake_object.run(text), int(re.search(r'(?<=_)\d+(?=\.)', filename).group(0))])
            papers_count += 1
    ranked_keywords = get_ranked_keywords(result, papers_count)
    return ranked_keywords


def main(name, needs_convert):
    name = str(name).replace(' ', '_')
    needs_convert = int(needs_convert)
    # Convert pdf to txt if needed
    if needs_convert:
        path = '/home/paula/Descargas/Memoria/extractpapers/pdfs/{}/'.format(name)
        txt_path = convert_all(path)
    else:
        txt_path = '/home/paula/Descargas/Memoria/parsepapers/txt/{}/'.format(name)

    # Get ranked keywords from all the papers
    ranked_keywords = get_all_keywords(txt_path)

    # Write to file
    output_path = '/home/paula/Descargas/Memoria/parsepapers/keywords/{}/{}.txt'.format(name, str(datetime.datetime.now()))
    output_path_top500 = '/home/paula/Descargas/Memoria/parsepapers/keywords/{}/{}_500.txt'.format(name, str(datetime.datetime.now()))
    make_dir(output_path)
    make_dir(output_path_top500)
    output_file = open(output_path, "w")  # make text file
    output_file_top500 = open(output_path_top500, "w")  # make text file
    for k, v in ranked_keywords:
        output_file.write("{} {}\n".format(k, v))

    # Top 500
    top_100_keywords = list(ranked_keywords[0:500])
    shuffle(top_100_keywords)
    bin_searcher = Searcher('enwiki-latest-all-titles-in-ns0')
    tfidf_calc = TfidfCalculator("/home/paula/Descargas/Memoria/parsepapers/txt/*/",
                                 [element[0] for element in top_100_keywords])
    tfidf = tfidf_calc.get_tfidf_feats(name)
    for element in top_100_keywords:
        is_in_wiki = 1 if bin_searcher.find(element[0].replace(' ', '_')) else 0
        output_file_top500.write("{},{},{},{},{},{},{}\n".format(element[0], element[1][0], tfidf[element[0]], is_in_wiki, element[1][1], element[1][2], element[1][3]))
    output_file.close()
    output_file_top500.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

# classifier: define features
# of tf idf? some
# anyway we would need features
# basis from tf idf, score from rake, does the keyword appear in wikipedia? (to see if it's too specific)
# how to do this (api, or list of urls from wikipedia)

# year it was published first and latest

# number/ratio of docs the keyword was included [done]

# phrase depth 1 -prob(word appearing)
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