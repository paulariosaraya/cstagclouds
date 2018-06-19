from extractkeywords.features import rake
from extractkeywords.keyword import Keyword
import glob
import os
import re
from extractkeywords.features.tfidf import TfidfCalculator
from learningtorank.select_keywords import select_keywords
from extractkeywords.features.wiki_url import Searcher


class AuthorKeywords:
    def __init__(self, directory, author, filtered):
        self.author = author
        self.dir = directory
        self.papers_count = 0
        if filtered:
            self.rake_object = rake.Rake("/home/paula/Descargas/Memoria/extractkeywords/features/SmartStoplist.txt", 3, 4, 3)
        else:
            self.rake_object = rake.Rake("/home/paula/Descargas/Memoria/extractkeywords/features/SmartStoplist_original.txt", 3, 4, 3)
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
        return sorted(keywords_dict.items(), key=lambda x: x[1].rake_score, reverse=True)

    def get_keywords(self):
        return self.keywords

    def get_selected_keywords(self, model_path):
        # Wiki searcher
        bin_searcher = Searcher('/home/paula/Descargas/Memoria/extractkeywords/features/enwiki-latest-all-titles-in-ns0')

        # Tfidf cal
        tfidf_calc = TfidfCalculator("/home/paula/Descargas/Memoria/extractkeywords/txt/*/",
                                     [element[0] for element in self.keywords])
        tfidf = tfidf_calc.get_tfidf_feats(self.author)

        # Data for classifier
        x = []
        for key, keyword in self.keywords:
            keyword.set_is_in_wiki(1 if bin_searcher.find(key.replace(' ', '_')) else 0)
            keyword.set_tfidf(tfidf[key])
            x.append(keyword.get_features())
        return select_keywords([element[0] for element in self.keywords], x, model_path, [self.author for l in self.keywords])