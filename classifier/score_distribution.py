from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

import glob


def count_scores(path):
    scores = []
    for filename in glob.glob(path):
        with open(filename) as scores_file:
            for line in scores_file:
                line = line.split(',')
                scores.append(int(line[-1].strip()))
    return scores


labels, values = zip(*Counter(count_scores('/home/paula/Descargas/cstagclouds/extractkeywords/training/*')).items())

indexes = np.arange(len(labels))
width = 1

plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels)
plt.show()
