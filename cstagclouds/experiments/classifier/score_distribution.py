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


labels, values = zip(*Counter(count_scores('/home/paula/Descargas/tagclouds-api/cstagclouds/extractkeywords/training/*')).items())

values = [value for _,value in sorted(zip(labels,values))]
print(values)


labels = sorted(labels)
print(labels)


indexes = np.arange(len(labels))
width = 1

fig, ax = plt.subplots(1, 1)
barlist = ax.bar(indexes, values, color='#539caf')
colors = ["#BB7A98", "#BB7A98", "#BB7A98", "#BB7A98", "#BB7A98"]

for bar, color in zip(barlist, colors):
    bar.set_facecolor(color)

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax.set_axisbelow(True)
plt.xticks(indexes, labels)
# plt.xticks(indexes + width * 0.5, labels)
plt.ylabel('Cantidad de keywords')
plt.xlabel('Puntaje asignado')


plt.show()
