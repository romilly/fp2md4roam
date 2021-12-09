import os
from lxml import etree
import string

from lxml.etree import Element

from fp2md4roam.filing import FSFiler
from markdown_builder.document import MarkdownDocument
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
        root = fm.find('node')
        self.document = MarkdownDocument(indentation='\t\t')
        self.visit_node(root, -1)
        self.filer.write(file_name(self.get_title(root)), self.document.contents())
        self.document.close()

    def visit_node(self, node: Element, depth: int):
        if depth >= 0:
            self.convert(node, depth)
        for child in node.findall('node'):
            self.visit_node(child, depth+1)

    def convert(self, node: Element, depth: int):
        title = self.get_title(node)
        link_text = node.get('LINK')
        if link_text is None:
            self.document.append_bullet(title, depth)
            return
        if link_text.startswith('http'):
            self.document.append_bulleted_link(title, link_text, depth)
            return

    def get_title(self, node):
        title = node.get('TEXT')
        rich_nodes = node.findall('richcontent')
        for element in rich_nodes:
            if element.get('TYPE') == "NODE":
                title = convert_html2text(element)
                continue
            if element.get('TYPE') == "DETAILS":
                title += '\n' + convert_html2text(element)
            if element.get('TYPE') == "NOTE":
                title += '\n' + convert_html2text(element)
        return title


def convert_html2text(element):
    return html2text(tostring(element).decode('utf-8'))


    


