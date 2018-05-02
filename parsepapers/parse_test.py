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


def is_binary(filename):
    f = os.popen('file -bi '+filename, 'r')
    file_type = f.read()
    if file_type.startswith('text'):
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
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


def convert_all(path):
    path_base = "{}/txt/{}".format(os.path.dirname(os.path.realpath(__file__)), path.split("/")[-2])
    for filename in glob.glob(os.path.join(path, '*')):
        print(filename)
        path_split = os.path.split(filename)
        text_filename = "{}/{}.txt".format(path_base, path_split[1])
        if is_binary(filename) and not os.path.exists(text_filename):
            try:
                text = convert(filename)
                text = clean(text)
                write_text(text, text_filename)
            except PDFSyntaxError:
                print(filename)
            except Exception:
                print(filename)

    return path_base


def get_ranked_keywords(keywords):
    counter = Counter()
    for keyword in keywords:
        counter[keyword[0]] += keyword[1]
    return counter.most_common()


def get_all_keywords(txt_path):
    rake_object = rake.Rake("SmartStoplist.txt", 3, 5, 3)
    text = []
    for filename in glob.glob(os.path.join(txt_path, '*.txt')):
        with open(filename, 'r') as paper_file:
            paper_text = paper_file.read()
            text.append(paper_text)
    full_text = " ".join(text)
    print(full_text)
    keywords = rake_object.run(full_text)
    ranked_keywords = get_ranked_keywords(keywords)
    return ranked_keywords


def main(name):
    name = str(name).replace(' ', '_')
    txt_path = '/home/paula/Descargas/Memoria/parsepapers/txt/{}/'.format(name)

    # Get ranked keywords from all the papers
    ranked_keywords = get_all_keywords(txt_path)

    # Write to file
    output_path = '/home/paula/Descargas/Memoria/parsepapers/keywords/{}/{}.txt'.format(name, str(datetime.datetime.now()))
    output_path_shuffle = '/home/paula/Descargas/Memoria/parsepapers/keywords/{}/{}_shuffled.txt'.format(name, str(datetime.datetime.now()))
    make_dir(output_path)
    make_dir(output_path_shuffle)
    output_file = open(output_path, "w")  # make text file
    for k, v in ranked_keywords:
        output_file.write("{} {}\n".format(k, v))
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[1])

# classifier: define features
# of tf idf? some
# anyway we would need features
# basis from tf idf, score from rake, does the keyword appear in wikipedia? (to see if it's too specific)
# how to do this (api, or list of urls from wikipedia)
# year it was published