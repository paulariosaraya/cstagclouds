import glob
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class TfidfCalculator:
    def __init__(self, directory, vocabulary):
        self.corpus = []
        self.authors = {}
        self.set_corpus(directory)
        self.tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), stop_words='english', vocabulary=vocabulary, token_pattern=r"(?u)\b[\w-]+\b")
        self.tfidf_matrix = self.tf.fit_transform(self.corpus)
        self.feature_names = self.tf.get_feature_names()

    def set_corpus(self, directory):
        i = 0
        for papers_dir in glob.glob(directory):
            self.authors[papers_dir.split('/')[-2]] = i
            author_text = []
            for filename in glob.glob(os.path.join(papers_dir, '*.txt')):
                with open(filename, 'r') as paper_file:
                    author_text.append(paper_file.read())
            self.corpus.append("".join(author_text))
            i += 1

    # https://buhrmann.github.io/tfidf-analysis.html
    def get_tfidf_feats(self, author):
        ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
        dense = self.tfidf_matrix.todense()
        row = dense[self.authors[author]].tolist()[0]
        ids = np.argsort(row)[::-1]
        top_feats = {self.feature_names[i]: row[i] for i in ids}
        return top_feats
