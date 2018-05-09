from extractkeywords.utils import remove_ligatures


def extract_scores(path):
    scores = {}
    with open(path) as scores_file:
        for line in scores_file:
            (key, val) = line.split(',')
            scores[remove_ligatures(key)] = val.strip()
    return scores


def get_score(keyword, scores):
    if keyword in scores:
        return scores[keyword]
    else:
        return 0