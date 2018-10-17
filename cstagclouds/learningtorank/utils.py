import glob
import pickle

from sklearn.preprocessing import scale


def load_data(directory):
    x = []
    y = []
    w = []
    q = []
    rake = []
    i = 0
    groups = []
    for score_path in glob.glob(directory):
        i += 1
        with open(score_path, 'r') as paper_file:
            for line in paper_file:
                groups.append(i)
                line = line.split(',')
                target = int(line[-1].strip())
                line[5] = int(line[6]) - int(line[5])
                x.append(list(map(lambda x: float(x), line[1:-2])))
                y.append(target)
                w.append(line[0])
                q.append(score_path.split('/')[-1])
                rake.append(float(line[1]))
    return scale(x), y, w, q, rake, groups


def finalize(model, x, y, qids, filename):
    model.fit(x, y, qids)
    pickle.dump(model, open(filename, 'wb'))