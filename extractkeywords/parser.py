import glob
import os
import re
from io import BytesIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

from extractkeywords.utils import make_dir


def convert(filename):
    if not is_pdf(filename):
        raise Exception('File is not PDF')
    output = BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(filename, 'rb')
    num_pages = 0
    for page in PDFPage.get_pages(infile):
        if num_pages > 60:
            raise Exception('Page limit')
        interpreter.process_page(page)
        num_pages += 1
    infile.close()
    converter.close()
    text = clean_text(output.getvalue())
    output.close()
    return text


def is_pdf(filename):
    f = os.popen('file -bi ' + filename, 'r')
    file_type = f.read()
    if not file_type.startswith('application/pdf'):
        print(file_type)
        return False
    else:
        return True


def clean_text(text):
    text = text.decode('utf-8')
    text = re.sub(r'(\w+)(-\s+)(\w+(\s|[,;.]))', r'\1\3\n', text, flags=re.MULTILINE)
    return text


def write_text(text, text_filename):
    make_dir(text_filename)
    with open(text_filename, 'w') as f:
        f.write(text)


def convert_all(path):
    path_base = "{}/txt/{}".format(os.path.dirname(os.path.realpath(__file__)), path.split("/")[-2])
    for filename in glob.glob(os.path.join(path, '*')):
        path_split = os.path.split(filename)
        text_filename = "{}/{}.txt".format(path_base, path_split[1])
        if not os.path.exists(text_filename):
            try:
                text = convert(filename)
                write_text(text, text_filename)
            except PDFSyntaxError:
                print(filename)
            except Exception as e:
                print(filename, e)
    return path_base
