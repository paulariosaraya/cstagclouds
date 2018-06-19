from random import randint

import numpy as np
import pyltr
import sys
from pysofia.compat import RankSVM
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut

from learningtorank.learning_to_rank import LearningToRank
from learningtorank.utils import load_data, finalize
import pickle


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

    print("---- Cross val ----")
    for train_index, test_index in logo.split(x, y, groups):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        q_train, q_test = qids[train_index], qids[test_index]
        rake_train, rake_test = rake[train_index], rake[test_index]
        if save_model:
            model = RankSVM()
            model.fit(x_train, y_train, q_train)
            pickle.dump(model, open('%sRankSVM/rankSVM_model_%s.sav' % (model_dir, q_test[0].replace('.txt','')), 'wb'))
        else:
            model = pickle.load(open('%sRankSVM/rankSVM_model_%s.sav' % (model_dir, q_test[0].replace('.txt','')), 'rb'))
        pred_test = model.predict(x_test)
        print('%s' % (metric.calc_mean(q_test, y_test, pred_test)))

    # print("---- Random train test ----")
    # model = RankSVM()
    # gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=randint(0,30))
    # for train_index, test_index in gss.split(x, y, groups=groups):
    #     x_train, x_test = x[train_index], x[test_index]
    #     y_train, y_test = y[train_index], y[test_index]
    #     q_train, q_test = qids[train_index], qids[test_index]
    #     w_train, w_test = words[train_index], words[test_index]
    #     rake_train, rake_test = rake[train_index], rake[test_index]
    #     model.fit(x_train, y_train, q_train)
    #
    #     pred_test = model.predict(x_test)
    #     a = list(zip(q_test, pred_test, w_test))
    #     a2 = sorted(a, key=lambda x: (x[0], x[1]))
    #     for word in a2:
    #         print(word[0], word[1], word[2])
    #     print('Random ranking:', metric.calc_mean_random(q_test, y_test))
    #     print('Our model:', metric.calc_mean(q_test, y_test, pred_test))
    #     print('Rake:', metric.calc_mean(q_test, y_test, rake_test))
    #
    # print("---- Finalize ----")
    # model.fit(x, y, qids)
    # pickle.dump(model, open("%srankSVM_model.sav" % model_dir, 'wb'))


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))