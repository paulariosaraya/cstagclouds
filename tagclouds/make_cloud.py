import random

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from heapq import nlargest
from operator import itemgetter


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, 15%%)"


# def reorder(keywords):
#     new_keywords = {}
#     i =
#     for name, score in nlargest(10, keywords.items(), key=itemgetter(1)):
#         new_keywords[name] =


def make_cloud(selected_keys, model_name, author):
    print(len(selected_keys))
    print(selected_keys)
    wc = WordCloud(background_color="white", max_words=40)
    wc.generate_from_frequencies(selected_keys)

    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.axis("off")
    plt.title("40 with %s" % model_name)
    plt.show()

    wc.to_file('/home/paula/Descargas/Memoria/Examples/%s/%s_filtered_40tags_grey.png' % (author, model_name))