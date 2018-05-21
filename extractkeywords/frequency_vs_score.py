from extractkeywords.df import DfCalculator
import matplotlib.pyplot as plt

keywords_dir = "/home/paula/Descargas/Memoria/extractkeywords/training/Barcel=oacute=:Pablo.txt"
keywords = {}
frequencies2 = []
with open(keywords_dir, 'r') as file:
    for line in file:
        line = line.split(',')
        keywords[line[0].strip().replace('.','')] = int(line[-1].strip())
        frequencies2.append([line[0].strip().replace('.',''), float(line[2].strip())])


directory = "/home/paula/Descargas/Memoria/extractkeywords/txt/*/"

df_calc = DfCalculator(directory, list(keywords.keys()))

frequencies = sorted(df_calc.get_df_feats(), key = lambda x: int(x[1]), reverse=True)
frequencies2 = sorted(frequencies2, key = lambda x: x[1])

print(frequencies)
print(frequencies2)

rank_df = {}
current = 1
prev = frequencies[0][1]
score_sum = 0
for i in range(1,len(frequencies)+1):
    score_sum += keywords[frequencies[i-1][0]]
    if frequencies[i-1][1] < prev:
        prev = frequencies[i-1][1]
        current = i
    # if current in rank:
    #     rank[current].append(str(keywords[frequencies[i-1][0]])+frequencies[i-1][0])
    # else:
    #     rank[current] = [str(keywords[frequencies[i-1][0]])+frequencies[i-1][0]]
    rank_df[current] = score_sum / i


rank_tfidf = {}
current = 1
prev = 0
score_sum = 0
for i in range(1,len(frequencies2)+1):
    score_sum += keywords[frequencies2[i-1][0]]
    if frequencies2[i-1][1] > prev:
        prev = frequencies2[i-1][1]
        current = i
    # if current in rank:
    #     rank[current].append(str(keywords[frequencies[i-1][0]])+frequencies[i-1][0])
    # else:
    #     rank[current] = [str(keywords[frequencies[i-1][0]])+frequencies[i-1][0]]
    rank_tfidf[current] = score_sum / i

plt.plot(rank_tfidf.keys(), rank_tfidf.values())
plt.plot(rank_df.keys(), rank_df.values())
plt.show()