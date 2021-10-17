import os
from lxml import etree

from fp2md4roam.filing import RoamFileMaker
from fp2md4roam.markdown_document import MarkdownDocument
from fp2md4roam.node import Node
from html2text import html2text
from xml.etree.ElementTree import tostring


class RawMap:
    def __init__(self, map_contents: str, map_location: str):
        self.map_contents = map_contents
        self.map_location = map_location

    def map_directory(self):
        return os.path.split(self.map_location)[0]


def read(name: str):
    with open(name) as inp:
        result = inp.read()
    return result


class RoamWriter:
    def __init__(self, filer: RoamFileMaker):
        self.filer = filer
        self.filer.create_dirs()

    def append_text(self, text, depth):
        if text is None:
            return
        text = (depth*'\t\t')+text+'\n'
        self.current_document.append_text(text)

    def start_markdown_document(self, document: MarkdownDocument):
        self.current_document = document

    def finish_document(self):
        self.filer.file_document(self.current_document.file_name(), self.current_document.contents())

    def add_converted_html(self, html, depth):
        if html is not None and len(html):
            html_raw = tostring(html).decode('utf-8')
            html_text = html2text(html_raw)
            self.append_text(html_text, depth)

    def append_link(self, title, link_text, depth):
        self.append_text('- [%s](%s)' % (title, link_text), depth)

    def append_bullet(self, title, depth):
        if title is None:
            return
        self.append_text('- '+title, depth)


class Author:
    LANGUAGES = {
        'sh': 'bash',
        'c': 'c',
        'py': 'python',
        'js': 'javascript',
    }

    def __init__(self, filer: RoamFileMaker):
        self.writer = RoamWriter(filer)

    def visit(self, raw_map: RawMap):
        fm = etree.XML(raw_map.map_contents)
        root = Node(fm.find('node'), raw_map.map_directory())
        document = MarkdownDocument(root.get('TEXT'))
        self.writer.start_markdown_document(document)
        self.visit_node(root, -1)
        self.writer.finish_document()

    def visit_node(self, node: Node, depth: int):
        if depth >= 0:
            self.convert(node, depth)
        for child in node.children():
            self.visit_node(child, depth+1)

    def convert(self, node: Node, depth: int):
        title = node.get('TEXT')
        rich_nodes = node.map_node.findall('richcontent')
        for element in rich_nodes:
            if element.get('TYPE') == "NODE":
                title = html2text(tostring(element).decode('utf-8'))
                continue
            if element.get('TYPE') == "DETAILS":
                title += '\n'+html2text(tostring(element).decode('utf-8'))
        link_text = node.get('LINK')
        if link_text is None:
            self.writer.append_bullet(title, depth)
            return
        if link_text.startswith('http'):
            self.writer.append_link(title, link_text, depth)
            return

    @staticmethod
    def read_from_map_link(node: Node):
        link_text = node.get('LINK')
        file_source = os.path.join(node.map_directory, link_text)
        text = read(file_source)
        return text

    


