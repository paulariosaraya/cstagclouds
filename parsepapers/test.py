# -*- coding: utf-8 -*-

import re
from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode

import rake


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
    output.close
    return text


text = convert("978-3-319-25010-6_15")  # get string of text content of pdf
text = re.sub(r'(\w+)(-\s+)(\w+\s)', r'\1\3\n', text, flags=re.MULTILINE)
text = unidecode(unicode(text, encoding = "utf-8"))

textFilename = "978-3-319-25010-6_15.txt"
textFile = open(textFilename, "w")  # make text file
textFile.write(text)  # write text to text file
textFile.close()


rake_object = rake.Rake("SmartStoplist.txt", 3, 2, 4)

keywords = rake_object.run(text)
print "Keywords:", keywords