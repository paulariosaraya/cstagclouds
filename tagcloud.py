import glob
import os
import sys
import time
from random import shuffle

from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
from extractpapers.main import extract_papers, extract_dynamic
from tagclouds.make_cloud import make_cloud

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_all_samples():
    examples_dir = os.path.join(__location__, 'examples/*/')
    for author_dir in glob.glob(examples_dir):
        url = author_dir[:-1]
        make_tag_cloud(url, 0, 0)


def make_tag_cloud(url, needs_convert, is_filtered):
    print("Start process (%s)" % time.strftime("%H:%M:%S"))
    name = str(url).split('/')[-1]
    print(name)
    needs_convert = int(needs_convert)
    # Convert pdf to txt if needed
    if needs_convert:
        path = '%s/pdfs/%s/' % (os.getcwd(), name)
        if not os.path.exists(path):
            extract_papers(name)
        txt_path = convert_all(path)
        print("Finished converting papers (%s)" % time.strftime("%H:%M:%S"))
    else:
        txt_path = os.path.join(__location__, 'extractkeywords/txt/{}/'.format(name))

    print(txt_path)

    # Get ranked keywords from all the papers
    author_keywords = AuthorKeywords(txt_path, name, is_filtered)
    author_keywords.extract_keywords()

    print("Finished extracting keywords (%s)" % time.strftime("%H:%M:%S"))

    # [print(e[0], e[1].rake_score) for e in author_keywords.keywords]

    labels = ["A", "B", "C", "D", "E", "F"]
    shuffle(labels)

    if is_filtered:
        filter_type = "filtered"
    else:
        filter_type = "unfiltered"
    models = ["LinearRegression", "RankSVM", "LambdaMART", "AdaRank"]
    i = 0
    for model_name in models:
        model_path_author = os.path.join(__location__, "learningtorank/models/%s/%s/%s_model_%s.sav" % (
            filter_type, model_name, model_name[0].lower() + model_name[1:], name))
        if os.path.exists(model_path_author):
            model_path = model_path_author
        else:
            model_path = os.path.join(__location__, "learningtorank/models/%s/%s_model.sav" % (
                filter_type, model_name[0].lower() + model_name[1:]))

        selected = author_keywords.get_selected_keywords(model_path)
        label = labels[i]
        make_cloud(selected, model_name, name, filter_type, label)
        print("Finished making clouds for %s (%s)" % (model_name, time.strftime("%H:%M:%S")))
        i += 1

    # make rake cloud
    make_cloud(author_keywords.select_rake_keywords(), "rake", name, filter_type, labels[4])

    # make random cloud
    make_cloud(author_keywords.select_100_keywords(), "random", name, filter_type, labels[5])


make_tag_cloud("https://dblp.uni-trier.de/pers/hd/h/Hogan:Aidan", 0, 0)