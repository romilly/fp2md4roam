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

    def get_attribute(self, name):
        attributes = self.map_node.xpath('attribute[@NAME="%s"]' % name)
        if len(attributes) == 0:
            return None
        return attributes[0].get('VALUE')

    def icons(self):
        result = []
        icons = self.map_node.findall('icon')
        if len(icons):
            for icon in icons:
                result.append(icon.get('BUILTIN'))
        return result
