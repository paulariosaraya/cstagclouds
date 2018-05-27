import glob

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
import mord as m
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing, model_selection
from sklearn.tree import DecisionTreeClassifier


class ThreshClassifier:
    def __init__(self, directory, threshold, classifier):
        self.threshold = threshold
        self.data = self.load_data(directory)
        self.clf = classifier
        self.X_train, self.X_validation, self.Y_train, self.Y_validation = train_test_split(self.data['data'],
                                                                                            self.data['target'],
                                                                                            test_size=.2,
                                                                                            random_state=7)
        self.model = None

    def load_data(self, directory):
        data = {}
        data['feature_names'] = ["rake", "tfidf", "isinwiki", "ratio", "first_year", "last_year"]
        data['target_names'] = ["<=" + str(self.threshold), ">" + str(self.threshold)]
        data['data'] = []
        data['target'] = []
        data['word'] = []
        for score_path in glob.glob(directory):
            with open(score_path, 'r') as paper_file:
                print(score_path)
                for line in paper_file:
                    line = line.split(',')
                    target = int(line[-1].strip())
                    line[7] = int(line[6])-int(line[5])
                    data['data'].append(list(map(lambda x: float(x), line[1:-1])))
                    data['target'].append(1 if target > self.threshold else 0)
                    data['word'].append(line[0])
        return data

    def cross_val(self):
        scores = cross_val_score(self.clf, self.data['data'], self.data['target'], cv=12)
        print(scores)

    def train(self, test_size=0.33, random_state=42):
        train, test, train_target, test_target, train_words, test_words = train_test_split(self.data['data'],
                                                                                           self.data['target'],
                                                                                           self.data['word'],
                                                                                           test_size=test_size,
                                                                                           random_state=random_state)
        self.model = self.clf.fit(train, train_target)

    def grid_search_cv(self, tuned_parameters, scores, test_size=0.33, random_state=42):
        train, test, train_target, test_target, train_words, test_words = train_test_split(self.data['data'],
                                                                                           self.data['target'],
                                                                                           self.data['word'],
                                                                                           test_size=test_size,
                                                                                           random_state=random_state)
        for score in scores:
            print("# Tuning hyper-parameters for %s" % score)
            print()

            clf = GridSearchCV(self.clf, tuned_parameters, cv=10,
                               scoring=score)
            clf.fit(train, train_target)

            print("Best parameters set found on development set:")
            print()
            print(clf.best_params_)
            print()
            print("Grid scores on development set:")
            print()
            means = clf.cv_results_['mean_test_score']
            stds = clf.cv_results_['std_test_score']
            for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                print("%0.3f (+/-%0.03f) for %r"
                      % (mean, std * 2, params))
            print()

            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            y_true, y_pred = test_target, clf.predict(test)
            print(classification_report(y_true, y_pred))
            print(clf.best_params_)
        self.set_parameters(**clf.best_params_)

    def set_parameters(self, params):
        self.clf.set_params(**params)

    def predict(self):
        return self.clf.predict(np.array(self.data['data']))

    def fit_all(self):
        self.model = self.clf.fit(self.data['data'], self.data['target'])


def main():
    # clf = SVC(gamma=0.01, C=1000)
    # clf = GaussianNB()
    # clf = RandomForestClassifier(n_estimators=30)
    # clf = KNeighborsClassifier()
    # clf = DecisionTreeClassifier()
    thresh_clf = ThreshClassifier('/home/paula/Descargas/Memoria/extractkeywords/training/*', 2,
                                  make_pipeline(StandardScaler(), BaggingClassifier(SVC(C=10, gamma=0.1), n_estimators=15)))
    # Set the parameters by cross-validation
    # tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.1, 1e-2, 1e-3, 1e-4, 1e-5],
    #                      'C': [1, 10, 100, 1000, 10000]},
    #                     {'kernel': ['linear'], 'C': [1, 10, 100, 1000, 10000]}]
    #
    # scores = ['precision', 'recall']
    # print(thresh_clf.grid_search_cv(tuned_parameters, scores))
    # thresh_clf.set_parameters({'C': 10, 'kernel': 'rbf', 'gamma': 0.1})

    # parameters = {'n_estimators': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15)}
    # score = ['precision']
    # thresh_clf.grid_search_cv(tuned_parameters, scores)

    print("---- Cross val ----")
    thresh_clf.cross_val()

    print("\n---- Final predictions ----")
    thresh_clf.fit_all()
    final_predictions = thresh_clf.predict()
    for i in range(0, len(final_predictions)):
        if final_predictions[i] == thresh_clf.data['target'][i] and final_predictions[i] == 1:
            print(thresh_clf.data['word'][i])
    print(thresh_clf.clf.score(thresh_clf.data['data'], thresh_clf.data['target']))
    print(classification_report(thresh_clf.data['target'],final_predictions))


def main2():
    thresh_clf = ThreshClassifier('/home/paula/Descargas/Memoria/extractkeywords/training/*', 2,
                                  make_pipeline(StandardScaler(), SVC(C=10, gamma=0.1)))
    X_train = thresh_clf.X_train
    Y_train = thresh_clf.Y_train
    models = []
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1, gamma=0.1))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1, gamma=0.01))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1, gamma=0.001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=10, gamma=0.1))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=10, gamma=0.01))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=10, gamma=0.001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=10, gamma=0.0001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=100, gamma=0.1))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=100, gamma=0.01))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=100, gamma=0.001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=100, gamma=0.0001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1000, gamma=0.1))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1000, gamma=0.01))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1000, gamma=0.001))))
    models.append(('SVM Scale', make_pipeline(StandardScaler(), SVC(C=1000, gamma=0.0001))))
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=7)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)


if __name__ == "__main__":
    main()

# scores = cross_val_score(clf,data['data'],data['target'],cv=12)
# print(scores)
#
#
# model = clf.fit(train, train_target)
#
# preds = clf.predict(np.array(test))
# correct = {}
# incorrect = {}
# for i in range(0, len(preds)):
#     if preds[i] == test_target[i]:
#         correct[test_words[i]] = preds[i]
#     else:
#         incorrect[test_words[i]] = preds[i]
# print("---- Correct ----")
# for k,v in correct.items():
#     print("{}: {}".format(k,v))
# print("\n---- Incorrect ----")
# for k,v in incorrect.items():
#     print("{}: {}".format(k, v))
#
# print(accuracy_score(test_target, preds))
# print(classification_report(test_target, preds))
#
#
# print("\n---- Final predictions ----")
# final_predictions = clf.predict(np.array(data['data']))
# for i in range(0, len(final_predictions)):
#     if final_predictions[i] == data['target'][i] and final_predictions[i] == 1:
#         print(data['word'][i])
# print(clf.score(data['data'], data['target']))
# print(classification_report(data['target'],final_predictions))