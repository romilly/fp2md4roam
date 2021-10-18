import os
from os.path import normpath
import shutil


class FSFiler():
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def write(self, path: str, text: str):
        path = self.target_file(path)
        with open(path, 'w') as md:
            md.write(text)

    def target_file(self, file_name):
        path = os.path.join(self.target_directory, file_name)
        return path

    def create_dirs(self):
        os.makedirs(self.target_directory, exist_ok=True)

    def copy_file(self, source_path, target_file_name):
        target_path = normpath(self.target_file(target_file_name))
        source_path = normpath(source_path)
        if source_path == target_path: # pragma: no cover
            return
        shutil.copyfile(source_path, target_path)



