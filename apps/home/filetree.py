import math
import os
import pathlib
import zipfile

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def is_zip(path):
    paths = path.split('/')
    i = 0
    path = ''
    while i <= len(paths)-1:
        if paths[i].split('.')[-1] == 'zip':
            path = '/'.join(paths[:i+1])
            break
        i+=1
    return i<len(paths)-1, i, path # zip or not, index, path

class FileTree():
    """
        Class for creating a directory tree that keeps track of 
        parent directory as well as children
    """

    def __init__(self, full_path):
        self.full_path = full_path  # Full path of folder
        self.contents = []  # Contains all of the subfolders and files
        self.size = []  # Size of all the files
        self.type = []  # Type of files

        # Appends all subfolders and files to contents
        dir = os.path.normpath(full_path)

        self.curr_path = dir.replace('\\', '\\\\')
        a, b, c = is_zip(dir)
        print(a,b,c)
        if zipfile.is_zipfile(dir):
            zip_file = zipfile.ZipFile(dir)
            files = zipfile.Path(dir)
            for file in files.iterdir():
                self.size.append(convert_size(zip_file.getinfo(file.name if file.is_file() else file.name+'/').file_size))
                self.contents.append(file)
                if file.is_file():
                    self.type.append(file.name.split('.')[-1].lower())
                else:
                    self.type.append('dir')
        for path in pathlib.Path(dir).glob('*'):
            self.contents.append(path)
            self.size.append(convert_size(os.path.getsize(path)))
            if path.is_file():
                self.type.append(os.path.splitext(path)[1].lower())
            else:
                self.type.append('dir')

    def get_contents(self):
        """Returns contents of the folder in a list of strings"""
        return self.contents

    def get_size(self):
        """Returns contents of the folder in a list of strings"""
        return self.size

    def get_type(self):
        """Returns contents of the folder in a list of strings"""
        return self.type

    def get_current_path(self):
        return self.curr_path
