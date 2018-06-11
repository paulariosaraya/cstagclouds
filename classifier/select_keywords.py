import pickle


def select_keywords(words, x):
    load_model = pickle.load(open('/home/paula/Descargas/Memoria/classifier/ltr_model.sav', 'rb'))
    predictions = load_model.predict(x)
    result = {}
    for i in range(0, len(predictions)):
        result[words[i]] = predictions[i]
    print(result)
    return result
