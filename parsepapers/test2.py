# -*- coding: utf-8 -*-

import re
from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode


from rake_nltk import Rake

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


text = convert("1202.0984.pdf")  # get string of text content of pdf
text = re.sub(r'(\w+)(-\s+)(\w+\s)', r'\1\3\n', text, flags=re.MULTILINE)
text = unidecode(unicode(text, encoding = "utf-8"))

textFilename = "1202.0984.txt"
textFile = open(textFilename, "w")  # make text file
textFile.write(text)  # write text to text file
textFile.close()

r = Rake()
r.extract_keywords_from_text(text)
print "Keywords with scores: ", r.get_ranked_phrases_with_scores()
