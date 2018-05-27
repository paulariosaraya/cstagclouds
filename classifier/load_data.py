import glob
from random import shuffle

from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import mord as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


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
    # data['word'] = []
    data['rake_score'] = []
    data['tfidf'] = []
    data['isinwiki'] = []
    data['ratio'] = []
    data['first_year'] = []
    data['last_year'] = []
    data['year_dif'] = []
    data['class'] = []
    all_data = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.strip().split(',')
                line[7] = int(line[6])-int(line[5])
                line[5] = int(line[5]) - 1995
                line[6] = int(line[6]) - 2004
                all_data.append(line[1:-1])
                data['class'].append(1 if int(line[-1]) > threshold else 0)
    min_max_scaler = preprocessing.StandardScaler()
    all_data = min_max_scaler.fit_transform(all_data)
    for line in all_data:
        data['rake_score'].append(float(line[0]))
        data['tfidf'].append(float(line[1]))
        data['isinwiki'].append(int(line[2]))
        data['ratio'].append(float(line[3]))
        data['first_year'].append(int(line[4]))
        data['last_year'].append(int(line[5]))
        data['year_dif'].append(float(line[6]))
    return pd.DataFrame(data)


dataset = load_data('/home/paula/Descargas/Memoria/extractkeywords/training/*', 2)
print(dataset.shape)
print(dataset.head(20))
print(dataset.describe())
print(dataset.groupby('class').size())

# dataset.plot(kind='box', subplots=True, layout=(2,4), sharex=False, sharey=False)
# plt.show()

dataset.hist()
plt.show()

pd.scatter_matrix(dataset)
plt.show()
