import re


class DataReader(object):
    def __init__(self, path):
        self.path = path
        try:
            file = open(path, "r")
            self.content = file.read()
            file.close()
        except IOError:
            raise ValueError("A valid path is required.")

    def find_all(self, pattern):
        muster = re.compile(pattern, re.DOTALL)
        return muster.findall(self.content)
