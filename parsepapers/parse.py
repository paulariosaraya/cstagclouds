# coding=utf-8
from __future__ import print_function

import glob
import os
import re
from cStringIO import StringIO
from collections import Counter

import sys

import datetime
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode

import rake


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
    text = re.sub(r'(\w+)(-\s+)(\w+(\s|[,;.]))', r'\1\3\n', text, flags=re.MULTILINE)
    text = unidecode(unicode(text, encoding="utf-8"))
    return text


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def convert_all(path):
    path_base = "{}/txt/{}".format(os.path.dirname(os.path.realpath(__file__)), path.split("/")[-2])
    for filename in glob.glob(os.path.join(path, '*')):
        if is_binary(filename):
            try:
                text = convert(filename)
                text = clean(text)
                path_split = os.path.split(filename)
                text_filename = "{}/{}.txt".format(path_base, path_split[1])
                write_text(text, text_filename)
            except Exception:
                print(filename)
                print(Exception)

    return path_base


def get_ranked_keywords(keywords):
    counter = Counter()
    for keyword in keywords:
        counter[keyword[0]] += keyword[1]
    return counter.most_common()


def get_all_keywords(txt_path, output_path):
    keywords = []
    rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 3)
    for filename in glob.glob(os.path.join(txt_path, '*.txt')):
        with open(filename, 'r') as paper_file:
            text = paper_file.read()
            keywords += rake_object.run(text)
    ranked_keywords = get_ranked_keywords(keywords)
    output_file = open(output_path, "w")  # make text file
    for k,v in ranked_keywords:
        output_file.write("{} {}\n".format(k,v))
    output_file.close()


def main(name, needs_convert):
    name = str(name).replace(' ', '_')
    needs_convert = int(needs_convert)
    if needs_convert:
        path = '/home/paula/Descargas/Memoria/extractpapers/pdfs/{}/'.format(name)
        txt_path = convert_all(path)
    else:
        txt_path = '/home/paula/Descargas/Memoria/parsepapers/txt/{}/'.format(name)
    output_path = '/home/paula/Descargas/Memoria/parsepapers/keywords/{}/{}.txt'.format(name, str(datetime.datetime.now()))
    make_dir(output_path)
    get_all_keywords(txt_path, output_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

# plural normalization shuffle