# coding=utf-8
import glob
import os
import re
from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode
from collections import Counter

import rake


def write_text(text, text_filename):
    textFile = open(text_filename, "w")  # make text file
    textFile.write(text)  # write text to text file
    textFile.close()


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

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def main():
    keywords = []
    path = '/home/paula/Descargas/Memoria/extractpapers/pdfs/Éric_Tanter/'
    rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 3)
    for filename in glob.glob(os.path.join(path, '*.pdf')):
        text = convert(filename)
        text = clean(text)
        k = rake_object.run(text)
        keywords += k
        print(filename , k)

    keyword_file = open('keywords_eric.txt', 'w+r')
    counter = Counter()
    for keyword in keywords:
        keyword_file.write(keyword[0]+'\n')
        counter[keyword[0]] += keyword[1]

    # keywords_final = rake_object.run(text_final)
    # print ("Keywords: ", keywords_final)

    # text = convert("978-3-319-25010-6_15")
    # text = convert("978-3-642-41338-4_18")
    # text = convert("1202.0984.pdf")  # get text content of pdf

    # text_filename = "1202.0984.txt"
    # write_text(text, text_filename)

    print "Common words:", counter.most_common()


if __name__ == "__main__":
    main()
