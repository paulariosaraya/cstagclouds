import random

from extractkeywords.features import rake
from extractkeywords.keyword import Keyword
import glob
import os
import re
from extractkeywords.features.tfidf import TfidfCalculator
from learningtorank.select_keywords import select_keywords
from extractkeywords.features.wiki_url import Searcher

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class AuthorKeywords:
    def __init__(self, directory, author, filtered):
        self.author = author
        self.dir = directory
        self.papers_count = 0
        if filtered:
            self.rake_object = rake.Rake(os.path.join(__location__, 'features/SmartStoplist.txt'), 3, 3, 3)
        else:
            self.rake_object = rake.Rake(os.path.join(__location__, 'features/SmartStoplist_original.txt'), 3, 3, 3)
        self.keywords = []

    def extract_keywords(self):
        result = []
        for filename in glob.glob(os.path.join(self.dir, '*.txt')):
            with open(filename, 'r') as paper_file:
                text = paper_file.read()
                keywords = self.rake_object.run(text)
                year = int(re.search(r'(?<=_)\d+(?=\.)', filename).group(0))
                result.append([keywords, year])
                self.papers_count += 1
        self.keywords = self.get_ranked_keywords(result)[0:500]

    def get_ranked_keywords(self, result, n=500):
        keywords_dict = {}
        for keywords, year in result:
            for keyword in keywords:
                if keyword[0] in keywords_dict:
                    keyword_obj = keywords_dict[keyword[0]]
                elif "-" in keyword[0] and keyword[0].replace('-','') in keywords_dict:
                    keyword_obj = keywords_dict[keyword[0].replace('-','')]
                else:
                    keyword_obj = Keyword(keyword[0])
                    keywords_dict[keyword_obj.keyword] = keyword_obj
                keyword_obj.add_features(keyword[1], self.papers_count, year, keyword[2])
        keywords_sorted = sorted(keywords_dict.items(), key=lambda x: x[1].rake_score, reverse=True)

        # Set last 2 features
        # Wiki searcher
        bin_searcher = Searcher(
            os.path.join(__location__, 'features/enwiki-latest-all-titles-in-ns0'))
        print([element[0] for element in keywords_sorted])
        # Tfidf cal
        tfidf_calc = TfidfCalculator(os.path.join(__location__, "txt/*/"),
                                     [element[0] for element in keywords_sorted])
        tfidf = tfidf_calc.get_tfidf_feats(self.author)

        # Data for classifier
        for key, keyword in keywords_sorted:
            keyword.set_is_in_wiki(1 if bin_searcher.find(key.replace(' ', '_')) else 0)
            keyword.set_tfidf(tfidf[key])

        return keywords_sorted

    def get_keywords(self):
        return self.keywords

    def get_selected_keywords(self, model_path):
        features = []
        keys = []
        for key, keyword in self.keywords:
            features.append(keyword.get_features())
            keys.append(key)
        return select_keywords(keys, features, model_path, [self.author for l in self.keywords])

    def select_100_keywords(self):
        top_500 = random.sample(self.keywords[0:500], 500)
        result = []
        i = 0
        for key, keyword in top_500:
            result.append([key, i])
            i += 1
        return result

    def select_rake_keywords(self):
        result = [[key, keyword.rake_score] for key, keyword in self.keywords[::-1]]
        return result


