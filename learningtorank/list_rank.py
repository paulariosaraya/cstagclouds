import glob
from random import randint

import numpy as np
import pyltr
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import scale

from classifier.learning2rank.rank.ListNet import ListNet

train_dir = '/home/paula/Descargas/Memoria/extractkeywords/training/*'

X = []
y = []
w = []
q = []
rake = []
i = 0
groups = []
for score_path in glob.glob(train_dir):
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
X = np.array(scale(X))
y = np.array(y)
q = np.array(q)
w = np.array(w)
rake = np.array(rake)

metric = pyltr.metrics.NDCG(k=10)

gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=randint(0,30))
for train_index, test_index in gss.split(X, y, groups=groups):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    q_train, q_test = q[train_index], q[test_index]
    w_train, w_test = w[train_index], w[test_index]
    rake_train, rake_test = rake[train_index], rake[test_index]
    model = ListNet()
    model.fit(X_train, y_train, tv_ratio=0.85)

    print(model.model.predict(X_test))

    # a = list(zip(q_test, pred_test, w_test))
    # a2 = sorted(a, key=lambda x: (x[0], x[1]))
    # for word in a2:
    #     print(word[0], word[1], word[2])
    # print('Random ranking:', metric.calc_mean_random(q_test, y_test))
    # print('Our model:', metric.calc_mean(q_test, y_test, pred_test))
    # print('Rake:', metric.calc_mean(q_test, y_test, rake_test))