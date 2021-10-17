import os
from os.path import normpath
import shutil


class FSFiler():
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def file(self, path: str, text: str):
        path = self.target_file(path)
        with open(path, 'w') as md:
            md.write(text)

    def target_file(self, file_name):
        path = os.path.join(self.target_directory, file_name)
        return path

    def create_dirs(self, local_path):
        os.makedirs(os.path.join(self.target_directory, local_path), exist_ok=True)

    def copy_file(self, source_path, target_file_name):
        target_path = normpath(self.target_file(target_file_name))
        source_path = normpath(source_path)
        if source_path == target_path: # pragma: no cover
            return
        shutil.copyfile(source_path, target_path)


class RoamFileMaker:
    MARKDOWN_FILE_DIRECTORY = 'markdown'
    IMAGES = os.path.join(MARKDOWN_FILE_DIRECTORY, 'images')

    def __init__(self, filer: FSFiler):
        self.filer = filer

    def file_document(self, file_name: str, text: str):
        path = os.path.join(self.MARKDOWN_FILE_DIRECTORY, file_name)
        self.filer.file(path, text)

    def target_directory(self):
        return self.filer.target_directory

    def create_dirs(self):
        self.filer.create_dirs(self.IMAGES)

    def copy_image(self, source_path: str, target_file_name: str):
        target_path = os.path.join(self.MARKDOWN_FILE_DIRECTORY, self.IMAGES, target_file_name)
        self.filer.copy_file(source_path, target_path)

    def relative_image_location(self, link_text):
        return os.path.join(self.IMAGES,
                            os.path.basename(link_text))
