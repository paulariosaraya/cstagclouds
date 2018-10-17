from random import randint

import numpy as np
import pickle
import pyltr
from sklearn.model_selection import LeaveOneGroupOut, GroupShuffleSplit

from cstagclouds.learningtorank.utils import load_data


class LearningToRank:
    def __init__(self, data_dir, model, metric):
        self.x, self.y, self.words, self.qids, self.rake, self.groups = (np.array(l) for l in load_data(data_dir))
        self.model = model
        self.metric = metric

    def cross_val(self, make_model, model_dir, save_model):
        logo = LeaveOneGroupOut()
        for train_index, test_index in logo.split(self.x, self.y, self.groups):
            x_train, x_test = self.x[train_index], self.x[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            q_train, q_test = self.qids[train_index], self.qids[test_index]
            rake_train, rake_test = self.rake[train_index], self.rake[test_index]
            if save_model:
                model = make_model()
                model.fit(x_train, y_train, q_train)
                pickle.dump(model, open('%sRankSVM/rankSVM_model_%s.sav' % (model_dir, q_test[0]), 'wb'))
            else:
                model = pickle.load(open('/home/paula/Descargas/Memoria/classifier/ltr_model.sav', 'rb'))
            pred_test = model.predict(x_test)
            print('%s' % (self.metric.calc_mean(q_test, y_test, pred_test)))

    def random_train_test(self):
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=randint(0,30))
        for train_index, test_index in gss.split(self.x, self.y, groups=self.groups):
            x_train, x_test = self.x[train_index], self.x[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            q_train, q_test = self.qids[train_index], self.qids[test_index]
            w_train, w_test = self.words[train_index], self.words[test_index]
            rake_train, rake_test = self.rake[train_index], self.rake[test_index]
            self.model.fit(x_train, y_train, q_train)

            pred_test = self.model.predict(x_test)
            a = list(zip(q_test, pred_test, w_test))
            a2 = sorted(a, key=lambda x: (x[0], x[1]))
            for word in a2:
                print(word[0], word[1], word[2])
            print('Random ranking:', self.metric.calc_mean_random(q_test, y_test))
            print('Our model:', self.metric.calc_mean(q_test, y_test, pred_test))
            print('Rake:', self.metric.calc_mean(q_test, y_test, rake_test))

    def finalize(self, filename):
        self.model.fit(self.x, self.y, self.qids)
        pickle.dump(self.model, open(filename, 'wb'))