# http://www.logarithmic.net/pfh/blog/01186620415


class Searcher:
    def __init__(self, filename):
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
            # print('--', mid, line)
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

        #result = []
        while True:
            line = self.f.readline().decode('utf-8').strip().lower()
            if not line or not line == string: break
            if line == string: return True
            #if line[-1:] == b'\n': line = line[:-1]
            #result.append(line[len(string):])
        return False
