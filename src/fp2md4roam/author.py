import os
from lxml import etree
import string

from fp2md4roam.filing import FSFiler
from markdown_builder.document import MarkdownDocument
from fp2md4roam.node import Node
from html2text import html2text
from xml.etree.ElementTree import tostring


TABLE = str.maketrans('', '', string.punctuation)


class RawMap:
    def __init__(self, map_contents: str, map_location: str):
        self.map_contents = map_contents
        self.map_location = map_location

    def map_directory(self):
        return os.path.split(self.map_location)[0]


def file_name(title):
    file_prefix = title.translate(TABLE).replace(' ','').replace('\n','')
    return '%s.md' % file_prefix


class Author:
    def __init__(self, filer: FSFiler):
        self.filer = filer
        self.document = None

    def visit(self, raw_map: RawMap):
        fm = etree.XML(raw_map.map_contents)
        root = Node(fm.find('node'), raw_map.map_directory())
        self.document = MarkdownDocument(indentation='\t\t')
        self.visit_node(root, -1)
        self.filer.write(file_name(root.get('TEXT')), self.document.contents())

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
                title = convert_html2text(element)
                continue
            if element.get('TYPE') == "DETAILS":
                title += '\n' + convert_html2text(element)
        link_text = node.get('LINK')
        if link_text is None:
            self.document.append_bullet(title, depth)
            return
        if link_text.startswith('http'):
            self.document.append_bulleted_link(title, link_text, depth)
            return


def convert_html2text(element):
    return html2text(tostring(element).decode('utf-8'))


    


