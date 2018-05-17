from extractkeywords.df import DfCalculator
import matplotlib.pyplot as plt


def get_key_score(file_path):
    keywords = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.split(',')
            keywords[line[0].strip().replace('.','')] = int(line[-1].strip())
    return keywords


directory = "/home/paula/Descargas/Memoria/extractkeywords/txt/*/"
keywords_dir = "/home/paula/Descargas/Memoria/extractkeywords/training/Hogan:Aidan.txt"
keywords = get_key_score(keywords_dir)


df_calc = DfCalculator(directory, list(keywords.keys()))
ld_idx = list(df_calc.vocabulary).index('van harmelen')
print(df_calc.array[:, ld_idx])

frequencies = sorted(df_calc.get_df_feats("Hogan:Aidan"), key = lambda x: int(x[1]), reverse=True)
print(frequencies)
rank = {}
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
    rank[current] = score_sum / i

print(rank)

plt.plot(rank.keys(), rank.values())
plt.show()