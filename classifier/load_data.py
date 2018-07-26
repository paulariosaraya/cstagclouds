import glob
from random import shuffle

from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
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
    # data['RAKE'] = []
    data['tf-idf'] = []
    data['¿Está en wikipedia?'] = []
    data['Proporción de apariciones'] = []
    # data['Primera aparición'] = []
    # data['Última aparición'] = []
    # data['Diferencia años'] = []
    data['Longitud de la frase'] = []
    # data['Puntaje'] = []
    all_data = []
    for score_path in glob.glob(directory):
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                line = line.strip().split(',')
                # data['Puntaje'].append(int(line[-1]))
                line[8] = int(line[7])
                line[7] = int(line[6])-int(line[5])
                all_data.append(line[1:])
    # min_max_scaler = preprocessing.StandardScaler()
    # all_data = min_max_scaler.fit_transform(all_data)
    for line in all_data:
        git # data['RAKE'].append(float(line[0]))
        data['tf-idf'].append(float(line[1]))
        data['¿Está en wikipedia?'].append(int(line[2]))
        data['Proporción de apariciones'].append(float(line[3]))
        # data['Primera aparición'].append(int(line[4]))
        # data['Última aparición'].append(int(line[5]))
        # data['Diferencia años'].append(float(line[6]))
        data['Longitud de la frase'].append(float(line[7]))
    return pd.DataFrame(data)


dataset = load_data('/home/paula/Descargas/tagclouds-api/cstagclouds/extractkeywords/training/*', 2)
print(dataset.shape)
print(dataset.head(20))
print(dataset.describe())
# print(dataset.groupby('Puntaje').size())

# plts = dataset.plot(kind='box', subplots=True, layout=(3,3), sharex=False, sharey=False, fontsize=7)
# plt.show()

dataset.hist(figsize=(11,11), color="#613969")
plt.show()
# #
# pd.scatter_matrix(dataset, figsize=(11,11))
# plt.xticks(size=8)
# plt.yticks(size=8)
# plt.show()
