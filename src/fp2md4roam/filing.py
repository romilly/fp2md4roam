import os


class FSFiler():
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def write(self, path: str, text: str):
        self.create_dirs()
        path = self.target_file(path)
        with open(path, 'w') as md:
            md.write(text)

    def target_file(self, file_name):
        path = os.path.join(self.target_directory, file_name)
        return path

    def create_dirs(self):
        os.makedirs(self.target_directory, exist_ok=True)

