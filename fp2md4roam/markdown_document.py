import string
from datetime import datetime
from io import StringIO

TABLE = str.maketrans('', '', string.punctuation)


class MarkdownDocument():
    def __init__(self, title):
        self._contents = StringIO()
        self.title = title
        self.new_page()
        self.append_heading(title, 0)

    def append_text(self, text: str):
        self._contents.write(text)

    @staticmethod
    def heading(text: str, depth: int):
        return '\n\n%s %s\n\n' % (((1 + depth) * '#'), text)

    def contents(self):
        result = self._contents.getvalue()
        self._contents.close()
        return result

    def new_page(self):
        self.append_text('\n\n\\newpage\n\n')

    def append_heading(self, text: str, depth: int):
        if text is None:
            print('ouch!')
        if len(text) > 0:
            self.append_text(self.heading(text, depth))

    def append_image_link(self, node_text, location, decoration):
        self.append_text('\n\n![%s](%s)%s\n\n' % (node_text, location, decoration))

    def file_name(self):
        return 'BrainRules.md' # TODO: derive from input file name






