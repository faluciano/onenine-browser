import math
import os
import pathlib


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class FileTree():
    """
        Class for creating a directory tree that keeps track of 
        parent directory as well as children
    """
    def __init__(self, prev, full_path, name):
        self.prev = prev # Parent folder 
        self.full_path = full_path # Full path of folder
        self.name = name # Name of folder
        self.contents = [] # Contains all of the subfolders and files
        self.size = [] # Size of all the files
        self.type = [] # Type of files

        # Appends all subfolders and files to contents
        dir = os.path.normpath(full_path)

        for path in pathlib.Path(dir).glob('*'):
            self.contents.append(path)
            self.size.append(convert_size(os.path.getsize(path)))
            if path.is_file():
                self.type.append(os.path.splitext(path)[1].lower())
            else:
                self.type.append('dir')

    def get_contents(self):
        """Returns contents of the folder in a list of strings"""
        ret = []
        for path in self.contents:
            ret.append(path)
        return ret

    def get_size(self):
        """Returns contents of the folder in a list of strings"""
        ret = []
        for path in self.size:
            ret.append(path)
        return ret

    def get_type(self):
        """Returns contents of the folder in a list of strings"""
        ret = []
        for path in self.type:
            ret.append(path)
        return ret

    def get_subfolders(self):
        """Returns a list of FileTree subfolders if any"""
        ret = []
        for path in self.contents:
            if path[0]:
                ret.append(path[1])
        return ret

