import collections
import csv
import doctest

class Node:
    def __init__(self, identifier, **attributes):
        self.node_identifier = identifier
        self.attributes = attributes

    def attributes(self):
        return self.attributes

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        self.attributes[key] = value

class Graph:

    def __init__(self):
        self.graph_nodes = {}
        self.graph_edges = collections.defaultdict(dict)

    def __len__(self):
        return len(self.graph_nodes)

    def add_node(self, node_id, **attributes):
        self.graph_nodes[node_id] = Node(identifier=node_id, **attributes)

    def node(self, node_id):
        return self.graph_nodes[node_id]

    def nodes(self):
        return [self.graph_nodes[node] for node in sorted(self.graph_nodes)]

def read_graph_from_csv(node_file, edge_file,unused=False):
    graph = Graph()
    attributes = {}
    with open(node_file, 'r') as f:
        header = next(f) 
        header = header.split(',')
        for att in header:
            attributes[att.strip('\n')] = None
        
        
        for line in f:
            atts = []
            line = line.split(',')
            for elt in line:
                atts.append(elt.strip('\n'))

            for i, elt in enumerate(attributes):
                attributes[elt] = atts[i]

            graph.add_node(line[0], **attributes)

    return graph
