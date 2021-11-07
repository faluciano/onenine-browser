import os

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

        # Appends all subfolders and files to contents
        dir = os.path.normpath(full_path)
        for path in os.listdir(dir):
            # Recursively construct the file tree
            if os.path.isdir(dir+'/'+path):
                self.contents.append((True, FileTree(self,full_path+"/"+path, path)))
            else:
                self.contents.append((False, path))

    def get_contents(self):
        """Returns contents of the folder in a list of strings"""
        ret = []
        for path in self.contents:
            if path[0]:
                ret.append(path[1].name)
            else:
                ret.append(path[1])
        return ret

    def get_subfolders(self):
        """Returns a list of FileTree subfolders if any"""
        ret = []
        for path in self.contents:
            if path[0]:
                ret.append(path[1])
        return ret