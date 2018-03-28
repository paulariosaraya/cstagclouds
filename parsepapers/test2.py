# -*- coding: utf-8 -*-

import re
from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode


from rake_nltk import Rake

text = """
Abstract. Hundreds of public SPARQL endpoints have been deployed
on the Web, forming a novel decentralised infrastructure for querying billions 
of structured facts from a variety of sources on a plethora of topics.
But is this infrastructure mature enough to support applications? For 427
public SPARQL endpoints registered on the DataHub, we conduct various 
experiments to test their maturity. Regarding discoverability, we find
that only one-third of endpoints make descriptive meta-data available,
making it difficult to locate or learn about their content and capabilities.
 Regarding interoperability, we find patchy support for established
SPARQL features like ORDER BY as well as (understandably) for new
SPARQL 1.1 features. Regarding efficiency, we show that the performance 
of endpoints for generic queries can vary by up to 3-4 orders of
magnitude. Regarding availability, based on a 27-month long monitoring 
experiment, we show that only 32.2% of public endpoints can be
expected to have (monthly) "two-nines" uptimes of 99-100%.
"""  # get string of text content of pdf
sentence_delimiters = re.compile(u'[\\[\\]\n\t\\-\\"\\(\\)\\\'\u2019\u2013]|[.!?,;:]\s')
sentences = sentence_delimiters.split(text)

print sentences;