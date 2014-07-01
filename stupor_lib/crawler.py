import os
from subprocess import Popen, PIPE

class Crawler(object):
    def __init__(self):
        pass

    # Use find in linux shell to get file list
    def crawl(self, path):
        file_list = []
        find_cmd = ["find", path, "-type", "f", "-print"]
        proc = Popen(find_cmd, stdout=PIPE)
        (stdout, stderr) = proc.communicate()
        file_list = (str(stdout).
                         lstrip("b'").
                         rstrip("'").
                         split("\\n"))
        return file_list

    # This is a slow version. Super inefficient
    def crawl_path(self, path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                self.crawl(os.path.join(root, dir))
            for file in files:
                if os.path.join(root, file) == root:
                    return
                if os.path.isfile(os.path.join(root, file)):
                    file_list.add(os.path.join(root, file))
        return file_list