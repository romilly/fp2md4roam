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
        self.current_document = None
        self.has_front_matter = False
        self.book_chapters = []
        self.sample_chapters = []
        self.filer.create_dirs()

    def append_text(self, text, depth=0):
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

    def add_image(self, link_text, map_directory, node_text):
        file_source = os.path.join(map_directory, link_text)
        self.filer.copy_image(file_source, os.path.basename(link_text))
        self.current_document.append_image_link(node_text,
                                                self.filer.relative_image_location(link_text))

    def append_code(self, code: str,  language: str):
        self.append_text('\n\n```%s\n' % language)
        self.append_text(code)
        self.append_text('\n```\n')

    def append_link(self, title, link_text, depth):
        self.append_text('[%s](%s)' % (title, link_text), depth)

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
        self.visit_node(root, 0)
        self.writer.finish_document()

    def visit_node(self, node: Node, depth: int):
        self.convert(node, depth)
        for child in node.children():
            self.visit_node(child, depth+1)
        # self.finish_converting(node)

    def convert(self, node: Node, depth: int):
        self.handle_link(node, depth)
        self.convert_html_in(node, depth)

    def handle_link(self, node: Node, depth: int):
        title = node.get('TEXT')
        link_text = node.get('LINK')
        if link_text is None:
            self.writer.append_bullet(title, depth)
            return
        if link_text.startswith('http'):
            _, extension = os.path.splitext(link_text)
            extension = extension[1:]
            if extension in ['jpg', 'jpeg', 'png', 'gif', 'svg']:
                self.writer.add_image(link_text,
                                      node.map_directory,
                                      node.get('TEXT'))
                return
            if extension in self.LANGUAGES:
                language = self.LANGUAGES[extension]
                code = self.get_code_span(node)
                self.writer.append_code(code, language)
                return
        # if extension == 'md':
        #     self.writer.append_text(self.read_from_map_link(node))
        self.writer.append_link(title, link_text, depth)
        return

    def convert_html_in(self, node: Node, depth: int):
        html = node.map_node.find('richcontent')
        self.writer.add_converted_html(html, depth)

    def get_code_span(self, node: Node):
        code = self.read_from_map_link(node)
        code_lines = code.split('\n')
        return '\n'.join(code_lines)

    @staticmethod
    def read_from_map_link(node: Node):
        link_text = node.get('LINK')
        file_source = os.path.join(node.map_directory, link_text)
        text = read(file_source)
        return text

    

