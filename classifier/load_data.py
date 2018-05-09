import glob
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import numpy as np
import matplotlib.pyplot as plt


def load_data(directory):
    data = {}
    data['feature_names'] = ["rake score","tfidf","isinwiki","ratio","first_year","last_year"]
    data['target_names'] = ["<=1",">1"]
    data['data'] = []
    data['target'] = []
    data['word'] = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.split(',')
                target = int(line[-1].strip())
                data['data'].append(list(map(lambda x: float(x), line[1:-1])))
                data['target'].append(1 if target > 2 else 0)
                data['word'].append(line[0]+score_path)
    return data


data = load_data('/home/paula/Descargas/Memoria/extractkeywords/training/*')
label_names = data['target_names']
labels = data['target']
feature_names = data['feature_names']
features = data['data']

#X_new = SelectKBest(chi2, k=5).fit_transform(data['data'], data['target'])
selector = SelectKBest(chi2, k=5).fit(data['data'], data['target'])

scores = -np.log10(selector.pvalues_)

# Plot the scores.  See how "Pclass", "Sex", "Title", and "Fare" are the best?
plt.bar(range(len(data['feature_names'])), scores)
plt.xticks(range(len(data['feature_names'])), data['feature_names'], rotation='vertical')
plt.show()


train, test, train_target, test_target, train_words, test_words = train_test_split(data['data'],
                                                                                   data['target'],
                                                                                   data['word'],
                                                                                   test_size=0.33,
                                                                                   random_state=42)

clf = SVC(gamma=0.00001, C=1000,probability=True)
#clf = GaussianNB()
#clf = RandomForestClassifier()
#clf = KNeighborsClassifier()
#clf = DecisionTreeClassifier()
model = clf.fit(train, train_target)

preds = clf.predict(test)
print(list(map(lambda x,y,z: [x,y,z], preds, test_words, test_target)))
#preds = clf.predict(test)
print(accuracy_score(test_target, preds))