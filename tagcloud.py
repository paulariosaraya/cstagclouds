import glob
import os
import re
import sys
import time

from cstagclouds.extractkeywords.author_keywords import AuthorKeywords
from cstagclouds.extractkeywords.parser import convert_all
from cstagclouds.extractpapers.main import extract_papers
from cstagclouds.tagclouds.make_cloud import make_cloud

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def clean_name(raw_name):
    last, first = str(raw_name).split('/')[-1].split(':')
    name = ("%s %s" % (first, last))
    name = re.sub(r'=([a-zA-Z])(acute|uml|slash|grave|tilde)=', '\g<1>', name)
    return name.replace('_', ' ').replace('=', ' ').strip()


def to_json(keywords):
    final_keywords = []
    for i in range(0, len(keywords)):
        key, value = keywords[i]
        final_keywords.append({"text": key, "value": i})
    return final_keywords


def to_dict(keywords):
    final_keywords = {}
    for i in range(0, len(keywords)):
        key, value = keywords[i]
        final_keywords[key] = i
    return final_keywords


def get_all_samples():
    examples_dir = os.path.join(__location__, 'examples/*/')
    for author_dir in glob.glob(examples_dir):
        url = author_dir[:-1]
        make_tag_cloud(url)


def make_tag_cloud(url, n=50):
    name = str(url).split('/')[-1]
    top_keys = get_tc_keywords(sys.argv[1], n=n, json=0)
    for model, keys in top_keys.items():
        make_cloud(keys, model, name)


def get_tc_keywords(url, is_filtered=0, n=50, json=1):
    print("Start process (%s)" % time.strftime("%H:%M:%S"))
    name = str(url).split('/')[-1]
    # Convert pdf to txt if needed
    txt_path = os.path.join(__location__, 'data/txt/{}/'.format(name))
    if not os.path.exists(txt_path):
        print(txt_path)
        path = os.path.join(__location__, 'data/pdfs/{}/'.format(name))
        if not os.path.exists(path):
            extract_papers(name)
        txt_path = convert_all(path)
        print("Finished converting papers (%s)" % time.strftime("%H:%M:%S"))

    # Get ranked keywords from all the papers
    author_keywords = AuthorKeywords(txt_path, name, is_filtered)
    author_keywords.extract_keywords()

    print("Finished extracting keywords (%s)" % time.strftime("%H:%M:%S"))

    selected_top_keys = {}

    if is_filtered:
        filter_type = "filtered"
    else:
        filter_type = "unfiltered"
    models = ["LinearRegression", "RankSVM", "LambdaMART", "AdaRank"]
    i = 0
    for model_name in models:
        model_path = os.path.join(__location__, "cstagclouds/learningtorank/models/%s/%s_model.sav" % (
            filter_type, model_name[0].lower() + model_name[1:]))
        selected = author_keywords.get_selected_keywords(model_path)
        if json == 1:
            selected_top_keys[model_name] = to_json(selected[-n:])
        else:
            selected_top_keys[model_name] = to_dict(selected[-n:])
        print("Finished making clouds for %s (%s)" % (model_name, time.strftime("%H:%M:%S")))
        i += 1

    # make rake cloud
    if json == 1:
        selected_top_keys["rake"] = to_json(author_keywords.select_rake_keywords()[-n:])
    else:
        selected_top_keys["rake"] = to_dict(author_keywords.select_rake_keywords()[-n:])
    return selected_top_keys


if __name__ == '__main__':
    make_tag_cloud(sys.argv[1], n=50)

