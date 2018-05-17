import glob
from random import shuffle

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import mord as m
import numpy as np


def divide_classes(directory, new_dir):
    data = [[], [], [], [], []]
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                target = int(line.split(',')[-1].strip())
                line = ",".join(line.split(',')[0:-1])+","+line.split(',')[-1]
                data[target - 1].append(line)

    for i in range (0,5):
        class_file_path = "{}class_{}.txt".format(new_dir, str(i+1))
        with open(class_file_path, 'w') as class_file:
            shuffle(data[i])
            for line in data[i]:
                class_file.write(line)


def load_data(directory, threshold):
    data = {}
    data['feature_names'] = ["rake score", "tfidf", "isinwiki", "ratio", "first_year", "last_year", "phrase_depth"]
    data['target_names'] = ["<=" + str(threshold), ">" + str(threshold)]
    # data['target_names'] = ["1","2","3","4","5"]
    data['data'] = []
    data['target'] = []
    data['word'] = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.split(',')
                target = int(line[-1].strip())
                data['data'].append(list(map(lambda x: float(x), line[1:-1])))
                data['target'].append(1 if target > threshold else 0)
                # for i in range(0, 4):
                #     data['target'][i].append(1 if target > i + 1 else 0)
                # data['real_class'].append(target)
                data['word'].append(line[0])
    return data


def load_csv(directory, new_csv):
    lines = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.split(',')
                lines.append(",".join(line[1:]))
    with open(new_csv, 'w') as csv:
        shuffle(lines)
        for line in lines:
            csv.write(line)

load_csv('/home/paula/Descargas/Memoria/classifier/training/*', '/home/paula/Descargas/Memoria/classifier/keywords.csv')

#divide_classes('/home/paula/Descargas/Memoria/extractkeywords/training/*', '/home/paula/Descargas/Memoria/classifier/training/')

# X_new = SelectKBest(chi2, k=5).fit_transform(data['data'], data['target'])
# selector = SelectKBest(chi2, k=5).fit(data['data'], data['target'])
#
# scores = -np.log10(selector.pvalues_)
#
# # Plot the scores'/home/paula/Descargas/Memoria/extractkeywords/training/*'
# plt.bar(range(len(data['feature_names'])), scores)
# plt.xticks(range(len(data['feature_names'])), data['feature_names'], rotation='vertical')
# plt.show()


# data = load_data('/home/paula/Descargas/Memoria/classifier/training/*', 2)
#
# train, test, train_target, test_target, train_words, test_words, train_class, test_class = train_test_split(data['data'],
#                                                                                                             data['target'],
#                                                                                                             data['word'],
#                                                                                                             data['real_class'],
#                                                                                                             test_size=0.33,
#                                                                                                             random_state=42)

# clf = SVC(gamma=0.00001, C=1000,probability=True)
# clf = GaussianNB()
# clf = RandomForestClassifier()
# clf = KNeighborsClassifier()
# clf = DecisionTreeClassifier()

# clf = m.LogisticIT()
# model = clf.fit(np.array(train), np.array(train_target))
#
# preds = clf.predict(np.array(test))
# print(list(map(lambda x,y,z: [x,y,z], preds, test_words, test_target)))
# print(accuracy_score(test_target, preds))
