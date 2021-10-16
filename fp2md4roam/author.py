import os
from abc import ABC, abstractmethod

from logzero import logger
from lxml import etree

from fp2md4roam.filing import RoamFileMaker
from fp2md4roam.markdown_document import MarkdownDocument
from fp2md4roam.visitor import MapVisitor
from fp2md4roam.node import Node
from html2text import HTML2Text
from xml.etree.ElementTree import tostring


class RoamWriter:
    def __init__(self, filer: RoamFileMaker):
        self.filer = filer
        self.html_converter = HTML2Text(out=self.append_text)
        self.current_document = None
        self.has_front_matter = False
        self.book_chapters = []
        self.sample_chapters = []
        self.filer.create_dirs()

    def append_text(self, text):
        self.current_document.append_text(text)

    def start_markdown_document(self, document: MarkdownDocument):
        self.current_document = document

    def finish_document(self):
        self.filer.file_document(self.current_document.file_name(), self.current_document.contents())

    def add_converted_html(self, html):
        if html is not None and len(html):
            html_text = tostring(html).decode('utf-8')
            self.html_converter.handle(html_text)

class NodeHandler(ABC):
    @abstractmethod
    def can_handle(self, node:Node):
        pass

    @abstractmethod
    def start_converting(self, node: Node):
        pass

    @abstractmethod
    def finish_converting(self, node: Node):
        pass


class PageHandler(NodeHandler):
    def __init__(self, writer: RoamWriter):
        self.writer = writer

    @classmethod
    def build(cls, writer: RoamWriter, *handler_classes):
        handlers = [handler_class(writer) for handler_class in handler_classes]
        return handlers

    def convert_html_in(self, node: Node):
        html = node.map_node.find('richcontent')
        self.writer.add_converted_html(html)

    def can_handle(self, node: Node):
        pass

    def start_converting(self, node: Node):
        pass

    def finish_converting(self, node: Node):
        pass


class RawMap:
    def __init__(self, map_contents: str, map_location: str):
        self.map_contents = map_contents
        self.map_location = map_location

    def map_directory(self):
        return os.path.split(self.map_location)[0]


class RootHandler(PageHandler):
    def can_handle(self, node: Node):
        return node.depth == 0

    def start_converting(self, node: Node):
        document = MarkdownDocument(node.get('TEXT'))
        self.writer.start_markdown_document(document)


    def finish_converting(self, node: Node):
        self.writer.finish_document()


class BulletPointHandler(PageHandler):
    def can_handle(self, node: Node):
        return node.depth > 0

    def start_converting(self, node: Node):
        pass

    def finish_converting(self, node: Node):
        pass


class Author(MapVisitor):
    def __init__(self, filer: RoamFileMaker):
        MapVisitor.__init__(self)
        writer = RoamWriter(filer)
        self.handlers = PageHandler.build(writer, RootHandler, BulletPointHandler)

    def visit(self, raw_map: RawMap):
        fm = etree.XML(raw_map.map_contents)
        root = Node(fm.find('node'), raw_map.map_directory())
        self.visit_node(root)

    def visit_node(self, node: Node):
        self.start_converting(node)
        for child in node.children():
            self.visit_node(child)
        self.finish_converting(node)

    def start_converting(self, node: Node):
        logger.debug('converting %s' % node)
        for handler in self.handlers:
            if handler.can_handle(node):
                handler.start_converting(node)
                return
        raise ValueError('cannot handle node %s depth:%d' % (node.get('TEXT'), node.depth)) # pragma: no cover

    def finish_converting(self, node):
        for handler in self.handlers:
            if handler.can_handle(node):
                handler.finish_converting(node)
                return
        raise ValueError('cannot handle node %s depth:%d' % (node.get('TEXT'), node.depth)) # pragma: no cover


