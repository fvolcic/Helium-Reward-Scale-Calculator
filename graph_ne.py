

class Attribute_Obj:
    def __init__(self, **attributes):
        self.attributes = attributes
    
    def __getitem__(self, key):
        return self.attributes[key]
    
    def __setitem__(self, key, value):
        self.attributes[key] = value

class Node(Attribute_Obj):
    """Class representing a graph node."""
    def __init__(self, **attributes):
        self.super.__init__(attributes)

class Edge(Attribute_Obj):
    """Class representing an edge."""
    def __init__(self, **attributes):
        self.super.__init__(attributes)

class BaseGraph:
"""A base class graph."""

    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def nodes(self): 
        """Return all the nodes in the graph."""
        return list(self.nodes.values())
    
    def add_node(self, node):
        self.nodes[node['name']] = node
    
def read_graph_from_csv(node_file, graph_file):
    """Read in nodes and edges from a file. Return a graph."""