from xml.etree.ElementTree import Element


class Node:
    def __init__(self, map_node: Element, map_directory: str, depth: int = 0):
        self.map_node = map_node
        self.map_directory = map_directory
        self.depth = depth

    def children(self):
        return [Node(child, self.map_directory, self.depth+1) for child in self.map_node.findall('node')]

    def get(self, name):
        return self.map_node.get(name)

