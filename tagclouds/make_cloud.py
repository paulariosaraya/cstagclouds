import matplotlib.pyplot as plt
from wordcloud import WordCloud

from extractkeywords.utils import make_dir


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


def make_cloud(selected_keys, model_name, author, filter_type, label, n=50):
    clouds_dir = '/home/paula/Descargas/Memoria/examples/%s/' % author
    make_dir(clouds_dir)

    print(n)
    selected_top_keys = normalize(selected_keys[-n:])
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
    plt.title("%s with %s (%s)" % (n, model_name, filter_type))
    plt.show()

    wc.to_file('%s%s_%s_%s_%dtags_grey.png' % (clouds_dir, label, model_name, filter_type, n))