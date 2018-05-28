import glob

import numpy as np
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import pickle


class ThreshClassifier:
    def __init__(self, directory, threshold, classifier):
        self.threshold = threshold
        self.X, self.Y, self.words = self.load_data(directory)
        self.clf = classifier
        self.X_train, self.X_test, self.Y_train, self.Y_test, self.words_train, self.words_test = train_test_split(
            self.X,
            self.Y,
            self.words,
            test_size=.25,
            random_state=7)
        self.model = None

    def load_data(self, directory):
        data = []
        targets = []
        words = []
        for score_path in glob.glob(directory):
            with open(score_path, 'r') as paper_file:
                print(score_path)
                for line in paper_file:
                    line = line.split(',')
                    target = int(line[-1].strip())
                    features = [line[1], line[2], line[4], line[6], int(line[6])-int(line[5]), line[7]]
                    data.append(list(map(lambda x: float(x), features)))
                    targets.append(1 if target > self.threshold else 0)
                    words.append(line[0])
        return data, targets, words

    def cross_val(self):
        kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=10)

        scores = cross_val_score(self.clf, self.X_train, self.Y_train, cv=kf, verbose=1)
        print(scores)

    def set_parameters(self, params):
        self.clf.set_params(**params)

    def predict(self, data):
        return self.clf.predict(np.array(data))

    def fit_train(self):
        self.model = self.clf.fit(self.X_train, self.Y_train)

    def finalize(self):
        self.model = self.clf.fit(self.X, self.Y)
        filename = 'finalized_model.sav'
        # pickle.dump(self.model, open(filename, 'wb'))


def main():
    clf = make_pipeline(StandardScaler(), BaggingClassifier(SVC(C=10, gamma=0.1), n_estimators=6))
    thresh_clf = ThreshClassifier('/home/paula/Descargas/Memoria/extractkeywords/training/*', 2, clf)

    print("---- Cross val ----")
    thresh_clf.cross_val()

    print("\n---- Test ----")
    thresh_clf.fit_train()
    print(thresh_clf.clf.score(thresh_clf.X_test, thresh_clf.Y_test))
    print(classification_report(thresh_clf.Y_test, thresh_clf.predict(thresh_clf.X_test)))

    print("\n---- Final predictions ----")
    thresh_clf.finalize()
    final_predictions = thresh_clf.predict(thresh_clf.X)
    print(final_predictions)
    for i in range(0, len(final_predictions)):
        if final_predictions[i] == 1:
            print(thresh_clf.words[i])
    print(thresh_clf.clf.score(thresh_clf.X, thresh_clf.Y))
    print(classification_report(thresh_clf.Y,final_predictions))


if __name__ == "__main__":
    main()