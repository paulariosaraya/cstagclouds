import os
import sys
import time

from extractkeywords.author_keywords import AuthorKeywords
from extractkeywords.parser import convert_all
from extractpapers.main import extract_papers, extract_dynamic
from tagclouds.make_cloud import make_cloud


def main(url, needs_convert, is_filtered):
    print("Start process (%s)" % time.strftime("%H:%M:%S"))
    name = str(url).split('/')[-1]
    needs_convert = int(needs_convert)
    # Convert pdf to txt if needed
    if needs_convert:
        path = '%s/pdfs/%s/' % (os.getcwd(), name)
        if not os.path.exists(path):
            recall, failed_downloads = extract_papers(name)
            print("Finished downloading papers (%s)" % time.strftime("%H:%M:%S"))
            print("recall = %d", recall)
            # time.sleep(0.5)
            # os.execl(sys.executable, sys.executable, *sys.argv)
            # if recall < 0.6:
            #     extract_dynamic(name, failed_downloads)
            #     print("Finished selenium PDFs extraction (%s)" % time.strftime("%H:%M:%S"))
        txt_path = convert_all(path)
        print("Finished converting papers (%s)" % time.strftime("%H:%M:%S"))
    else:
        txt_path = '/home/paula/Descargas/Memoria/extractkeywords/txt/{}/'.format(name)

    # Get ranked keywords from all the papers
    author_keywords = AuthorKeywords(txt_path, name, is_filtered)
    author_keywords.extract_keywords()

    print("Finished extracting keywords (%s)" % time.strftime("%H:%M:%S"))

    # [print(e[0], e[1].rake_score) for e in author_keywords.keywords]
    if is_filtered:
        filter_type = "filtered"
    else:
        filter_type = "unfiltered"
    models = ["LinearRegression", "RankSVM", "LambdaMART", "AdaRank"]
    for model_name in models:
        model_path_author = "/home/paula/Descargas/Memoria/learningtorank/models/%s/%s/%s_model_%s.sav" % (
            filter_type, model_name, model_name[0].lower() + model_name[1:], name)
        if os.path.exists(model_path_author):
            model_path = model_path_author
        else:
            model_path = "/home/paula/Descargas/Memoria/learningtorank/models/%s/%s_model.sav" % (
                filter_type, model_name[0].lower() + model_name[1:])

        selected = author_keywords.get_selected_keywords(model_path)
        make_cloud(selected, model_name, name, filter_type)
        print("Finished making clouds for %s (%s)" % (model_name, time.strftime("%H:%M:%S")))

    # make rake cloud
    make_cloud(author_keywords.select_rake_keywords(), "rake", name, filter_type)

    # make random cloud
    make_cloud(author_keywords.select_100_keywords(), "random", name, filter_type)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
