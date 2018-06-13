import matplotlib.pyplot as plt
from wordcloud import WordCloud


def make_cloud(selected_keys):
    print(len(selected_keys))
    print(selected_keys)
    wc = WordCloud(background_color="white", max_words=40)
    wc.generate_from_frequencies(selected_keys)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("40")
    plt.show()