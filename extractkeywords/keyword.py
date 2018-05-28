class Keyword:
    def __init__(self, word):
        self.keyword = word
        self.rake_score = 0
        self.tfidf = 0
        self.is_in_wiki = 0
        self.ratio = 0
        self.first_year = 3000000
        self.last_year = 0
        self.phrase_depth = 0
        self.score = 0

    def add_features(self, score, num_of_papers, year, phrase_depth):
        self.rake_score += score
        self.ratio += 1/num_of_papers
        self.first_year = min(self.first_year, year)
        self.last_year = max(self.last_year, year)
        self.phrase_depth += phrase_depth

    def set_tfidf(self, tfidf):
        self.tfidf = tfidf

    def set_is_in_wiki(self, is_in_wiki):
        self.is_in_wiki = is_in_wiki

    def set_score(self, scores):
        if self.keyword in scores:
            self.score = scores[self.keyword]

    def to_string(self):
        return "{},{},{},{},{},{},{},{}".format(self.keyword, self.rake_score, self.tfidf,
                                                self.is_in_wiki, self.ratio, self.first_year,
                                                self.last_year, self.phrase_depth)

    def get_features(self):
        return [self.rake_score, self.tfidf, self.ratio, self.last_year, self.last_year-self.first_year, self.phrase_depth]