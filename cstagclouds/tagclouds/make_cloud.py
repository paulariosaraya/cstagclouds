import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

from cstagclouds.extractkeywords.utils import make_dir

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % 15


# def reorder(keywords):
#     new_keywords = {}
#     i =
#     for name, score in nlargest(10, keywords.items(), key=itemgetter(1)):
#         new_keywords[name] =

def normalize(keywords):
    final_keywords = {}
    for i in range(0, len(keywords)):
        key, value = keywords[i]
        final_keywords[key] = i
    return final_keywords


def make_cloud(selected_top_keys, model_name, author, n=50):

    clouds_dir = os.path.join(__location__, 'clouds/%s/' % author)
    print(clouds_dir)
    make_dir(clouds_dir)

    # selected_top_keys = normalize(selected_keys[-n:])
    wc = WordCloud(background_color="white",
                   max_words=n,
                   prefer_horizontal=1,
                   width=1000,
                   height=500,
                   min_font_size=8,
                   max_font_size=120)
    wc.generate_from_frequencies(selected_top_keys)

    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.axis("off")
    plt.title("%s with %s" % (n, model_name))
    # plt.show()

    wc.to_file('%s%s_%dtags_grey.png' % (clouds_dir, model_name, n))