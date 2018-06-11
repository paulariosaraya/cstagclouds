import glob
import pickle
from random import randint

import numpy as np
import pyltr
from pysofia.compat import RankSVM
from sklearn.model_selection import LeaveOneGroupOut, GroupShuffleSplit
from sklearn.preprocessing import scale


def load_data(directory):
    X = []
    y = []
    w = []
    q = []
    rake = []
    i = 0
    groups = []
    for score_path in glob.glob(directory):
        i += 1
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                groups.append(i)
                line = line.split(',')
                target = int(line[-1].strip())
                line[5] = int(line[6]) - int(line[5])
                X.append(list(map(lambda x: float(x), line[1:-2])))
                y.append(target)
                w.append(line[0])
                q.append(score_path.split('/')[-1])
                rake.append(float(line[1]))
    return scale(X), y, w, q, rake, groups


class LearningToRank:
    def __init__(self, directory, model, metric):
        self.X, self.y, self.words, self.qids, self.rake, self.groups = (np.array(l) for l in load_data(directory))
        self.model = model
        self.metric = metric

    def cross_val(self):
        logo = LeaveOneGroupOut()
        for train_index, test_index in logo.split(self.X, self.y, self.groups):
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            q_train, q_test = self.qids[train_index], self.qids[test_index]
            rake_train, rake_test = self.rake[train_index], self.rake[test_index]
            model = pyltr.models.LambdaMART(
                metric=metric,
                n_estimators=1500,
                learning_rate=0.03,
                max_features=1,
                query_subsample=0.5,
                max_leaf_nodes=10,
                min_samples_leaf=64,
                verbose=1,
            )
            model.fit(X_train, y_train, q_train)
            pred_test = model.predict(X_test)
            print('| %s | %s | %s |' % (q_test[0],
                                        metric.calc_mean(q_test, y_test, pred_test),
                                        metric.calc_mean(q_test, y_test, rake_test)))

    def train_test(self):
        gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=randint(0, 30))
        for train_index, test_index in gss.split(self.X, self.y, groups=self.groups):
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            q_train, q_test = self.qids[train_index], self.qids[test_index]
            w_train, w_test = self.words[train_index], self.words[test_index]
            rake_train, rake_test = self.rake[train_index], self.rake[test_index]

            self.model.fit(X_train, y_train, q_train)

            pred_test = self.model.predict(X_test)
            a = list(zip(q_test, pred_test, w_test))
            a2 = sorted(a, key=lambda x: (x[0], x[1]))
            for word in a2:
                print(word[0], word[1], word[2])
            print('Random ranking:', self.metric.calc_mean_random(q_test, y_test))
            print('Our model:', self.metric.calc_mean(q_test, y_test, pred_test))
            print('Rake:', self.metric.calc_mean(q_test, y_test, rake_test))

    def finalize(self, filename):
        self.model = self.model.fit(self.X, self.y)
        pickle.dump(self.model, open(filename, 'wb'))


train_dir = '/home/paula/Descargas/Memoria/extractkeywords/training/*'
# model = RankSVM()
metric = pyltr.metrics.NDCG(k=10)
model = pyltr.models.LambdaMART(
    metric=metric,
    n_estimators=2000,
    learning_rate=0.03,
    max_features=1,
    query_subsample=0.5,
    max_leaf_nodes=10,
    min_samples_leaf=64,
    verbose=1,
)
ltr = LearningToRank(train_dir, model, metric)
ltr.cross_val()