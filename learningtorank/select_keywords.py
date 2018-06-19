import pickle

import numpy as np
from sklearn.preprocessing import scale


def select_keywords(words, x, model_path, qids):
    load_model = pickle.load(open(model_path, 'rb'))
    if "adaRank" in model_path:
        predictions = load_model.predict(np.array(scale(x)), np.array(qids))
    else:
        predictions = load_model.predict(np.array(scale(x)))
    result = {}
    for i in range(0, len(predictions)):
        result[words[i]] = predictions[i]
    print(result)
    return result
