import glob

import mord as m
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_data(directory, threshold):
    data = {}
    data['feature_names'] = ["rake score", "tfidf", "isinwiki", "ratio", "first_year", "last_year", "phrase_depth"]
    data['target_names'] = ["1","2","3","4","5"]
    data['data'] = []
    data['target'] = []
    data['word'] = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.split(',')
                target = int(line[-1].strip())
                data['data'].append(list(map(lambda x: float(x), line[1:-2])))
                data['target'].append(target)
                # for i in range(0, 4):
                #     data['target'][i].append(1 if target > i + 1 else 0)
                # data['real_class'].append(target)
                data['word'].append(line[0])
    return data

data = load_data('/home/paula/Descargas/Memoria/classifier/training/*', 2)

train, test, train_target, test_target, train_words, test_words = train_test_split(data['data'],
                                                                                                            data['target'],
                                                                                                            data['word'],
                                                                                                            test_size=0.33,
                                                                                                            random_state=42)

clf = m.LogisticSE()
model = clf.fit(np.array(train), np.array(train_target))

preds = clf.predict(np.array(data['data']))
print(list(map(lambda x,y,z: [x,y,z], preds, data['word'], data['target'])))
print(accuracy_score(data['target'], preds))
