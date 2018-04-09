# coding=utf-8
from __future__ import print_function
import glob
import os
import re

import parse


def get_keywords(text):
    pattern = re.compile(r'key[ ]?words:?((\n?.+)+)')
    sentences = text.split('.')
    keywords_list = []
    for sentence in sentences:
        keywords = pattern.search(sentence.lower())
        if keywords:
            keywords = keywords.group(1).strip().replace("\n", " ")
            keywords_list = re.split('[,;*]\s?', keywords)
            print (keywords)
            break
        if "introduction" in sentence.lower():
            break
    return keywords_list


def convert_all(path):
    for filename in glob.glob(os.path.join(path, '*')):
        text = parse.convert(filename)
        text = parse.clean(text)
        path_txt = filename.split("/")
        keywords = get_keywords(text)
        if len(keywords) > 0:
            parse.write_text("\n".join(keywords), "/home/paula/Descargas/Memoria/parsepapers/txt/Aidan_Hogan/" + path_txt[-1] + ".key")
        text_filename = "/home/paula/Descargas/Memoria/parsepapers/txt/Aidan_Hogan/" + path_txt[-1] + ".txt"
        parse.write_text(text, text_filename)
        print(filename)


def main():
    convert_all('/home/paula/Descargas/Memoria/extractpapers/pdfs/Aidan_Hogan/')


if __name__ == "__main__":
    main()
