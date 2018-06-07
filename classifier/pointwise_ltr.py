import glob

import mord as m
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
import pyltr

from sklearn.preprocessing import scale

directory = '/home/paula/Descargas/Memoria/extractkeywords/training/*'
X = []
y = []
words = []
qids = []
i = 1
div = 0
for score_path in glob.glob(directory):
    if i == 10:
        div = len(X)
    with open(score_path, 'r') as paper_file:
        i += 1
        for line in paper_file:
            line = line.split(',')
            target = int(line[-1].strip())
            # features = [line[1], line[2], line[4], line[6], int(line[6])-int(line[5]), line[7]]
            X.append(list(map(lambda x: float(x), line[1:-1])))
            y.append(target)
            words.append(line[0])
            qids.append(score_path.split('/')[-1])
X = scale(X)

X_train = np.array(X[0:div])
X_test = np.array(X[div:])
y_train = np.array(y[0:div])
y_test = np.array(y[div:])
w_train = np.array(words[0:div])
w_test = np.array(words[div:])
q_train = np.array(qids[0:div])
q_test = np.array(qids[div:])

clf = LinearRegression()
model = clf.fit(X_train, y_train)

pred_test = clf.predict(X_test)

metric = pyltr.metrics.NDCG(k=10)

a = list(zip(q_test, pred_test, w_test))
a2 = sorted(a, key=lambda x: (x[0], x[1]))
for word in a2:
    print(word[0], word[1], word[2])
print('Random ranking:', metric.calc_mean_random(q_test, y_test))
print('Our model:', metric.calc_mean(q_test, y_test, pred_test))
