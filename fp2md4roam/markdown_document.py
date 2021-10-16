import string
from io import StringIO

TABLE = str.maketrans('', '', string.punctuation)


class MarkdownDocument():
    def __init__(self, title):
        self._contents = StringIO()
        self.title = title
        self.append_text('- '+title)

    def append_text(self, text: str):
        self._contents.write(text)

    def contents(self):
        result = self._contents.getvalue()
        self._contents.close()
        return result


    def append_image_link(self, node_text, location, decoration):
        self.append_text('\n\n![%s](%s)%s\n\n' % (node_text, location, decoration))

    def file_name(self):
        return 'BrainRules.md' # TODO: derive from input file name





