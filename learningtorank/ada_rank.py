from random import randint

import numpy as np
import pyltr
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut

from learningtorank.adarank.adarank import AdaRank
from learningtorank.adarank.metrics import NDCGScorer
from learningtorank.utils import load_data

train_dir = '/home/paula/Descargas/Memoria/extractkeywords/training2/*'
x, y, words, qids, rake, groups = (np.array(l) for l in load_data(train_dir))

scorer = NDCGScorer(k=10)
metric = pyltr.metrics.NDCG(k=10)

logo = LeaveOneGroupOut()
print("---- Cross val ----")
for train_index, test_index in logo.split(x, y, groups):
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    q_train, q_test = qids[train_index], qids[test_index]
    rake_train, rake_test = rake[train_index], rake[test_index]
    model = AdaRank(max_iter=100, estop=10, scorer=scorer)
    model.fit(x_train, y_train, q_train)
    pred_test = model.predict(x_test, q_test)
    print('%s' % (metric.calc_mean(q_test, y_test, pred_test)))

# gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=randint(0, 30))
# for train_index, test_index in gss.split(x, y, groups=groups):
#     x_train, x_test = x[train_index], x[test_index]
#     y_train, y_test = y[train_index], y[test_index]
#     q_train, q_test = qids[train_index], qids[test_index]
#     w_train, w_test = words[train_index], words[test_index]
#     rake_train, rake_test = rake[train_index], rake[test_index]
#     model = AdaRank(max_iter=100, estop=10, scorer=scorer).fit(x_train, y_train, q_train)
#     pred_test = model.predict(x_test, q_test)
#     a = list(zip(q_test, pred_test, w_test))
#     a2 = sorted(a, key=lambda x: (x[0], x[1]))
#     for word in a2:
#         print(word[0], word[1], word[2])
#     print(scorer(y_test, pred_test, q_test).mean())
#     print('Random ranking:', metric.calc_mean_random(q_test, y_test))
#     print('Rake:', metric.calc_mean(q_test, y_test, rake_test))