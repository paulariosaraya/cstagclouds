import glob

import numpy as np
import pyltr
from pyltr.data.pairwise_transform import pairwise_transform
from sklearn import svm
from sklearn.preprocessing import scale

directory = '/home/paula/Descargas/Memoria/extractkeywords/training/*'
words = []
qids = []
rake = []
X = []
y = []
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
            rake.append(float(line[1]))
            y.append(target)
            words.append(line[0])
            qids.append(score_path.split('/')[-1])

X = np.array(scale(X))
y = np.array(y)
qids = np.array(qids)


X_train = np.array(X[0:div])
X_test = np.array(X[div:])
y_train = np.array(y[0:div])
y_test = np.array(y[div:])
w_train = np.array(words[0:div])
w_test = words[div:]
q_train = np.array(qids[0:div])
q_test = np.array(qids[div:])

X_train_p, y_train_p = pairwise_transform(X_train, y_train, q_train)
X_test_p, y_test_p = pairwise_transform(X_test, y_test, q_test)

metric = pyltr.metrics.NDCG(k=10)

clf = svm.SVC(kernel='linear', C=.1)
clf.fit(X_train_p, y_train_p)

pred = clf.predict(X_test_p)

print(clf.score(X_test_p, y_test_p))


def compare(x, y):
    pair = np.array([x[0] - y[0]])
    return clf.predict(pair)


def cmp_to_key(mycmp, val):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            if val is None:
                self.obj = obj
            else:
                self.obj = val[obj]
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

prev = ""
preds = dict()
for i in range(len(q_test)):
    if q_test[i] in preds:
        preds[q_test[i]].append((X_test[i], w_test[i]))
    else:
        preds[q_test[i]] = [(X_test[i], w_test[i])]

final_pred_list = {}
pred_test = []
for (key, val) in preds.items():
    sorted_words = sorted(val, key=cmp_to_key(compare, None))
    # print(key, sorted_words)
    # print([(i,sorted_words[i][1]) for i in range(len(sorted_words))])
    blah = sorted(range(len(val)), key=cmp_to_key(compare, val))
    rank = [0 for i in range(len(blah))]
    for i in range(len(blah)):
        rank[blah[i]] = i
    final_pred_list[key] = rank

prev = ""
for qid in q_test:
    if prev != qid:
        pred_test+=final_pred_list[qid]
        prev = qid

a = list(zip(q_test, pred_test, w_test))
a2 = sorted(a, key=lambda x: (x[0], x[1]))
for word in a2:
    print(word[0], word[1], word[2])

print('Random ranking:', metric.calc_mean_random(q_test, y_test))
print('Our model:', metric.calc_mean(q_test, y_test, pred_test))