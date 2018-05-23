import glob

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import mord as m
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing


def load_data(directory, threshold):
    data = {}
    data['feature_names'] = ["rake","tfidf", "isinwiki", "ratio", "first_year", "last_year", "phrase_depth"]
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
    data['data'] = preprocessing.scale(data['data'])
    return data


data = load_data('/home/paula/Descargas/Memoria/extractkeywords/training/*', 2)

train, test, train_target, test_target, train_words, test_words = train_test_split(data['data'],
                                                                                   data['target'],
                                                                                   data['word'],
                                                                                   test_size=0.33,
                                                                                   random_state=42)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.1, 1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [1, 10, 100, 1000, 10000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000, 10000]}]

scores = ['precision', 'recall']

# for score in scores:
#     print("# Tuning hyper-parameters for %s" % score)
#     print()
#
#     clf = GridSearchCV(SVC(), tuned_parameters, cv=10,
#                        scoring='%s_macro' % score)
#     clf.fit(train, train_target)
#
#     print("Best parameters set found on development set:")
#     print()
#     print(clf.best_params_)
#     print()
#     print("Grid scores on development set:")
#     print()
#     means = clf.cv_results_['mean_test_score']
#     stds = clf.cv_results_['std_test_score']
#     for mean, std, params in zip(means, stds, clf.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#               % (mean, std * 2, params))
#     print()
#
#     print("Detailed classification report:")
#     print()
#     print("The model is trained on the full development set.")
#     print("The scores are computed on the full evaluation set.")
#     print()
#     y_true, y_pred = test_target, clf.predict(test)
#     print(classification_report(y_true, y_pred))
#     print()

clf = SVC(gamma=0.01, C=1000)
# clf = GaussianNB()
# clf = RandomForestClassifier(n_estimators=30)
# clf = KNeighborsClassifier()
# clf = DecisionTreeClassifier()

# clf = m.LogisticIT()

scores = cross_val_score(clf,data['data'],data['target'],cv=12)
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
print(classification_report(test_target, preds))


print("\n---- Final predictions ----")
final_predictions = clf.predict(np.array(data['data']))
for i in range(0, len(final_predictions)):
    if final_predictions[i] == data['target'][i] and final_predictions[i] == 1:
        print(data['word'][i])
print(clf.score(data['data'], data['target']))
print(classification_report(data['target'],final_predictions))