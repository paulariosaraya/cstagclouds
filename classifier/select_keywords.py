import pickle


def select_keywords(words, x):
    load_model = pickle.load(open('/home/paula/Descargas/Memoria/classifier/finalized_model.sav', 'rb'))
    predictions = load_model.predict(x)
    result = {}
    for i in range(0, len(predictions)):
        if predictions[i] == 1:
            result[words[i]] = x[i][0] #(x[i][0] + x[i][1]) / 2
    print(result)
    return result
