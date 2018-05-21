import glob

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import mord as m
import numpy as np
from sklearn.model_selection import cross_val_score


def load_data(directory, threshold):
    data = {}
    data['feature_names'] = ["rake score", "tfidf", "isinwiki", "ratio", "first_year", "last_year", "phrase_depth"]
    data['target_names'] = ["<=" + str(threshold), ">" + str(threshold)]
    data['data'] = []
    data['target'] = []
    data['word'] = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.split(',')
                target = int(line[-1].strip())
                data['data'].append(list(map(lambda x: float(x), line[1:-1])))
                data['target'].append(1 if target > threshold else 0)
                data['word'].append(line[0])
    return data


data = load_data('/home/paula/Descargas/Memoria/classifier/training/*', 2)

train, test, train_target, test_target, train_words, test_words = train_test_split(data['data'],
                                                                                   data['target'],
                                                                                   data['word'],
                                                                                   test_size=0.33,
                                                                                   random_state=42)

clf = SVC(gamma=0.00001, C=1000, class_weight={0:.7, 1:.3})
# clf = GaussianNB()
# clf = RandomForestClassifier()
# clf = KNeighborsClassifier()
# clf = DecisionTreeClassifier()

#clf = m.LogisticIT()

scores = cross_val_score(clf,data['data'],data['target'],cv=13)
print(scores)


model = clf.fit(train, train_target)

preds = clf.predict(np.array(test))
correct = {}
incorrect = {}
for i in range(0, len(preds)):
    if preds[i] == test_target[i]:
        correct[test_words[i]] = preds[i]
    else:
        incorrect[test_words[i]] = preds[i]
print("---- Correct ----")
for k,v in correct.items():
    print("{}: {}".format(k,v))
print("\n---- Incorrect ----")
for k,v in incorrect.items():
    print("{}: {}".format(k, v))

print(accuracy_score(test_target, preds))
print(clf.score(test, test_target))