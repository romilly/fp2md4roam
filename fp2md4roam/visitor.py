import os
from abc import ABC, abstractmethod
from lxml import etree
from fp2md4roam.node import Node


class RawMap:
    def __init__(self, map_contents: str, map_location: str):
        self.map_contents = map_contents
        self.map_location = map_location

    def map_directory(self):
        return os.path.split(self.map_location)[0]


class MapVisitor(ABC):
    def __init__(self):
        self.map_directory = None

    def visit(self, raw_map: RawMap):
        fm = etree.XML(raw_map.map_contents)
        root = Node(fm.find('node'), raw_map.map_directory())
        self.visit_node(root)

    def visit_node(self, node: Node):
        # print('visiting %s with %d children' % (node, len(node.children())))
        self.start_converting(node)
        for child in node.children():
            self.visit_node(child)
        self.finish_converting(node)

    @abstractmethod
    def start_converting(self, node: Node):
        pass

    @abstractmethod
    def finish_converting(self, node):
        pass