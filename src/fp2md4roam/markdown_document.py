from io import StringIO


class MarkdownDocument:
    def __init__(self, title: str):
        self._contents = StringIO()
        self.title = title

    def append_text(self, text: str):
        self._contents.write(text)

    def append_text_indented(self, text, depth):
        text = (depth*'\t\t')+text+'\n'
        self.append_text(text)

    def append_link(self, title, link_text, depth):
        self.append_text_indented('- [%s](%s)' % (title, link_text), depth)

    def append_bullet(self, title, depth):
        self.append_text_indented('- '+title, depth)

    def contents(self):
        result = self._contents.getvalue()
        self._contents.close()
        return result







