import glob
import os
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
from extractkeywords.utils import singularize, remove_ligatures


def clean_text(text):
    text = re.sub(r'(\w+)(-\s+)(\w+(\s|[,;.]))', r'\1\3\n', text, flags=re.MULTILINE)
    return text


def pre_process(s):
    return singularize(remove_ligatures(s))


class DfCalculator:
    def __init__(self, directory, vocabulary):
        self.corpus = []
        self.authors = {}
        self.set_corpus(directory)
        self.cv = CountVectorizer(analyzer='word', ngram_range=(1, 3), vocabulary=vocabulary, token_pattern=r"(?u)\b[\w-]+\b", preprocessor=pre_process)
        self.cv_matrix = self.cv.fit_transform(self.corpus)
        self.feature_names = self.cv.get_feature_names()
        self.vocabulary = np.array(vocabulary)
        self.array = self.cv_matrix.toarray()

    def set_corpus(self, directory):
        i = 0
        self.corpus = []
        for papers_dir in glob.glob(directory):
            self.authors[papers_dir.split('/')[-2]] = i
            author_text = []
            for filename in glob.glob(os.path.join(papers_dir, '*.txt')):
                with open(filename, 'r') as paper_file:
                    author_text.append(clean_text(paper_file.read()))
            self.corpus.append("".join(author_text))
            i+=1

    # https://buhrmann.github.io/tfidf-analysis.html
    def get_df_feats(self, author):
        ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
        array = self.cv_matrix.toarray()
        sum = np.sum(array, axis=0) #- array[self.authors[author]]
        return list(zip(self.vocabulary, sum))

