from extractkeywords import rake
from extractkeywords.keyword import Keyword
import glob
import os
import re


class AuthorKeywords:
    def __init__(self, directory, author):
        self.author = author
        self.dir = directory
        self.papers_count = 0
        self.rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 3)
        self.keywords = {}

    def extract_keywords(self):
        result = []
        for filename in glob.glob(os.path.join(self.dir, '*.txt')):
            with open(filename, 'r') as paper_file:
                text = paper_file.read()
                keywords = self.rake_object.run(text)
                year = int(re.search(r'(?<=_)\d+(?=\.)', filename).group(0))
                result.append([keywords, year])
                self.papers_count += 1
        self.keywords = self.get_ranked_keywords(result)

    def get_ranked_keywords(self, result):
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
