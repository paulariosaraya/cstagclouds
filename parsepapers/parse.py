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
    output.close
    return text

def main():
    text = convert("978-3-642-41338-4_18")  # get string of text content of pdf
    text = clean(text)

    #text_filename = "978-3-319-25010-6_15.txt"
    #write_text(text, text_filename) # is this necessary???

    rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 4, 1, 4)
    keywords = rake_object.run(text)
    print "Keywords:", keywords

    print "Sentences:", rake.split_sentences(text)

    counter = Counter(text.strip().split())

    print "Common words:", counter.most_common()

if __name__ == "__main__":
    main()