import os
from abc import ABC, abstractmethod


class Filer(ABC):
    def __init__(self, target_directory: str):
        # self.directory_config = directory_config
        self.target_directory = target_directory

    @abstractmethod
    def file(self, path: str, text: str):
        pass

    @abstractmethod
    def create_dirs(self, local_path):
        pass


class FSFiler(Filer):
    def __init__(self, target_directory: str):
        Filer.__init__(self, target_directory)

    def file(self, path: str, text: str):
        path = self.target_file(path)
        with open(path, 'w') as md:
            md.write(text)

    def target_file(self, file_name):
        path = os.path.join(self.target_directory, file_name)
        return path

    def create_dirs(self, local_path):
        os.makedirs(os.path.join(self.target_directory, local_path), exist_ok=True)


class RoamFileMaker:
    MARKDOWN_FILE_DIRECTORY = 'markdown'
    IMAGES = os.path.join(MARKDOWN_FILE_DIRECTORY, 'images')

    def __init__(self, filer: Filer):
        self.filer = filer

    def file_document(self, file_name: str, text: str):
        path = os.path.join(self.MARKDOWN_FILE_DIRECTORY, file_name)
        self.filer.file(path, text)

    def target_directory(self):
        return self.filer.target_directory

    def create_dirs(self):
        self.filer.create_dirs(self.IMAGES)
