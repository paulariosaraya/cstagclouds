# http://www.logarithmic.net/pfh/blog/01186620415
import gzip
import os
import shutil
import urllib


def download_wiki_titles(filename):
    # urllib.request.urlretrieve("https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz",
    #                            filename + '.gz')
    with gzip.open(filename + '.gz', 'rb') as f_in:
        with open(filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


class Searcher:
    def __init__(self, filename):
        if not os.path.exists(filename):
            download_wiki_titles(filename)
        self.f = open(filename, 'rb')
        self.f.seek(0, 2)
        self.length = self.f.tell()

    def find(self, string):
        low = 0
        high = self.length
        while low < high:
            mid = (low + high) // 2
            p = mid
            while p >= 0:
                self.f.seek(p)
                if self.f.read(1) == b'\n': break
                p -= 1
            if p < 0: self.f.seek(0)
            line = self.f.readline().decode('utf-8').strip().lower()
            if line < string:
                low = mid + 1
            elif line > string:
                high = mid
            else:
                return True

        p = low
        while p >= 0:
            self.f.seek(p)
            if self.f.read(1) == b'\n': break
            p -= 1
        if p < 0: self.f.seek(0)

        while True:
            line = self.f.readline().decode('utf-8').strip().lower()
            if not line or not line == string: break
            if line == string: return True
        return False
