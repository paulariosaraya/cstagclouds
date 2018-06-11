import glob

import numpy as np
import pyltr
from pysofia.compat import RankSVM
from sklearn.model_selection import LeaveOneGroupOut, GroupShuffleSplit
from sklearn.preprocessing import scale

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
print(groups)
rake = np.array(rake)

metric = pyltr.metrics.NDCG(k=10)
logo = LeaveOneGroupOut()

print("| name      | model        | rake  |")
print("| ----------|:------------:| -----:|")
for train_index, test_index in logo.split(X, y, groups):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    q_train, q_test = q[train_index], q[test_index]
    rake_train, rake_test = rake[train_index], rake[test_index]
    model = RankSVM()
    model.fit(X_train, y_train, q_train)
    pred_test = model.predict(X_test)
    print('| %s | %s | %s |'%(q_test[0],
                            metric.calc_mean(q_test, y_test, pred_test),
                            metric.calc_mean(q_test, y_test, rake_test)))