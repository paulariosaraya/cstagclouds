import sys


def main(name, path):
    keywords_file = open(path, "r")  # make text file
    scores_file = open('/home/paula/Descargas/Memoria/parsepapers/scores/{}.csv'.format(name), "r")
    final_file = open('/home/paula/Descargas/Memoria/parsepapers/training/{}.txt'.format(name), "w")
    scores = {}
    for line in scores_file:
        (key, val) = line.split(',')
        scores[key] = val.strip()
    for line in keywords_file:
        try:
            score = scores[line.split(',')[0]]
        except KeyError:
            score = "None"
        final_file.write('{},{}\n'.format(line.strip(), score))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])