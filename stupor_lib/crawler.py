import os
import hashlib

class Crawler(object):
    def __init__(self, output='/tmp/duplicate_files.txt'):
        self.duplicate_files = {}
        self.hash_set = set()
        self.output_file = output
        self.hash_size = 1024 * 1024 * 1 # 1 Megabyte(s)
        pass

    def crawl(self, path):
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                self.crawl(os.path.join(root, dir))
            for file in files:
                self._hash_file(os.path.join(root, file))

    def save(self):
        f = open(self.output_file, 'w')
        for dup in self.duplicate_files:
            if len(self.duplicate_files[dup]) > 1:
                f.write("%s\t%s\n" % (dup, self.duplicate_files[dup]))
        f.close()

    def _hash_file(self, file_path):
        f = open(file_path, 'rb+')
        file_hash = hashlib.md5(f.read(self.hash_size)).hexdigest()
        f.close()
        if file_hash not in self.hash_set:
            self.hash_set.add(file_hash)
            self.duplicate_files[file_hash] = [file_path]
        else:
            if file_path not in self.duplicate_files[file_hash]:
                self.duplicate_files[file_hash].append(file_path)

