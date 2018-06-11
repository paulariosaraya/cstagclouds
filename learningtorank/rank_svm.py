import glob
from random import randint

import numpy as np
import pyltr
from pysofia.compat import RankSVM
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import scale

# train_dir = '/home/paula/Descargas/Memoria/classifier/train/*'
# test_dir = '/home/paula/Descargas/Memoria/classifier/test/*'
#
# X_train = []
# X_test = []
# y_train = []
# y_test = []
# w_train = []
# w_test = []
# q_train = []
# q_test = []
# rake_test = []
#
# for score_path in glob.glob(train_dir):
#     with open(score_path, 'r') as paper_file:
#         for line in paper_file:
#             line = line.split(',')
#             target = int(line[-1].strip())
#             # features = [line[1], line[2], line[4], line[6], int(line[6])-int(line[5]), line[7]]
#             line[5] = int(line[6]) - int(line[5])
#             X_train.append(list(map(lambda x: float(x), line[1:-2])))
#             y_train.append(target)
#             w_train.append(line[0])
#             q_train.append(score_path.split('/')[-1])
# X_train = np.array(scale(X_train))
# y_train = np.array(y_train)
# q_train = np.array(q_train)
#
# for score_path in glob.glob(test_dir):
#     with open(score_path, 'r') as paper_file:
#         for line in paper_file:
#             line = line.split(',')
#             target = int(line[-1].strip())
#             # features = [line[1], line[2], line[4], line[6], int(line[6])-int(line[5]), line[7]]
#             line[5] = int(line[6])-int(line[5])
#             X_test.append(list(map(lambda x: float(x), line[1:-2]))) #.append(int(line[6])-int(line[5])))
#             y_test.append(target)
#             w_test.append(line[0])
#             q_test.append(score_path.split('/')[-1])
#             rake_test.append(float(line[1]))
# X_test = np.array(scale(X_test))
# y_test = np.array(y_test)
# q_test = np.array(q_test)
# rake_test = np.array(scale(rake_test))

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
            # features = [line[1], line[2], line[4], line[6], int(line[6])-int(line[5]), line[7]]
            line[7] = int(line[6]) - int(line[5])
            X.append(list(map(lambda x: float(x), line[1:-1])))
            y.append(target)
            w.append(line[0])
            q.append(score_path.split('/')[-1])
            rake.append(float(line[1]))
X = np.array(scale(X))
y = np.array(y)
q = np.array(q)
w = np.array(w)
rake = np.array(rake)

gss = GroupShuffleSplit(n_splits=1, test_size=0.05, random_state=3)
for train_index, test_index in gss.split(X, y, groups=groups):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    q_train, q_test = q[train_index], q[test_index]
    w_train, w_test = w[train_index], w[test_index]
    rake_train, rake_test = rake[train_index], rake[test_index]

    metric = pyltr.metrics.NDCG(k=10)

    model = RankSVM()
    model.fit(X_train, y_train, q_train)

    pred_test = model.predict(X_test)
    a = list(zip(q_test, pred_test, w_test))
    a2 = sorted(a, key=lambda x: (x[0], x[1]))
    for word in a2:
        print(word[0], word[1], word[2])
    print('Random ranking:', metric.calc_mean_random(q_test, y_test))
    print('Our model:', metric.calc_mean(q_test, y_test, pred_test))
    print('Rake:', metric.calc_mean(q_test, y_test, rake_test))