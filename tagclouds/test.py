import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = {}
with open('/home/paula/Descargas/Memoria/extractkeywords/training/Hogan:Aidan.txt', 'r') as paper_file:
    for line in paper_file:
        line = line.split(',')
        target = int(line[-1].strip())
        if target > 1:
            text[line[0]] = (float(line[1])+float(line[2])) / 2

print(len(text))
print(text)
wc = WordCloud(background_color="white", max_words=35)
wc.generate_from_frequencies(text)

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()