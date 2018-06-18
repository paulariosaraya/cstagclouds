import pickle
import sys
from random import randint

import numpy as np
import pyltr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneGroupOut, GroupShuffleSplit

from learningtorank.utils import load_data, finalize


def main(filtered, save_model):
    if filtered:
        data_dir = '/home/paula/Descargas/Memoria/extractkeywords/training/*'
        model_dir = '/home/paula/Descargas/Memoria/learningtorank/models/Filtered/'
    else:
        data_dir = '/home/paula/Descargas/Memoria/extractkeywords/training_unfiltered/*'
        model_dir = '/home/paula/Descargas/Memoria/learningtorank/models/Unfiltered/'

    x, y, words, qids, rake, groups = (np.array(l) for l in load_data(data_dir))
    metric = pyltr.metrics.NDCG(k=10)
    logo = LeaveOneGroupOut()

    print(data_dir)

    # print("---- Cross val ----")
    # for train_index, test_index in logo.split(x, y, groups):
    #     x_train, x_test = x[train_index], x[test_index]
    #     y_train, y_test = y[train_index], y[test_index]
    #     q_train, q_test = qids[train_index], qids[test_index]
    #     rake_train, rake_test = rake[train_index], rake[test_index]
    #     if save_model:
    #         model = LinearRegression()
    #         model.fit(x_train, y_train)
    #         pickle.dump(model, open('%sLinearRegression/regression_model_%s.sav' % (model_dir, q_test[0]), 'wb'))
    #     else:
    #         model = pickle.load(open('%sLinearRegression/regression_model_%s.sav' % (model_dir, q_test[0]), 'rb'))
    #     pred_test = model.predict(x_test)
    #     print('%s' % metric.calc_mean(q_test, y_test, pred_test))

    print("---- Random train test ----")
    model = LinearRegression()
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=randint(0,30))
    for train_index, test_index in gss.split(x, y, groups=groups):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        q_train, q_test = qids[train_index], qids[test_index]
        w_train, w_test = words[train_index], words[test_index]
        rake_train, rake_test = rake[train_index], rake[test_index]
        model.fit(x_train, y_train)

        pred_test = model.predict(x_test)
        a = list(zip(q_test, pred_test, w_test))
        a2 = sorted(a, key=lambda x: (x[0], x[1]))
        for word in a2:
            print(word[0], word[1], word[2])
        print('Random ranking:', metric.calc_mean_random(q_test, y_test))
        print('Our model:', metric.calc_mean(q_test, y_test, pred_test))
        print('Rake:', metric.calc_mean(q_test, y_test, rake_test))

    print("---- Finalize ----")
    model.fit(x, y)
    pickle.dump(model, open("%sregression_model.sav" % model_dir, 'wb'))


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))