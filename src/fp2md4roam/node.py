from xml.etree.ElementTree import Element


class Node:
    def __init__(self, map_node: Element, map_directory: str=None):
        self.map_node = map_node
        # self.map_directory = map_directory

    def children(self):
        # return [Node(child, self.map_directory) for child in self.map_node.findall('node')]
        return [Node(child) for child in self.map_node.findall('node')]

    def get(self, name):
        return self.map_node.get(name)

